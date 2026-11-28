/**
 * Yazhi Pi extension.
 *
 * Thin harness adapter for the yazhi-purpose / yazhi-code skills. It does not
 * auto-commit, auto-push, or change tool permissions by itself. It adds five
 * commands that queue the matching skills and a few conservative safety gates
 * that follow the patterns in Pi's own examples.
 */

import {
  isToolCallEventType,
  type ExtensionAPI,
  type ExtensionContext,
} from "@earendil-works/pi-coding-agent";

type SkillCommand = {
  skill: string;
  mode?: string;
};

const SKILL_COMMANDS: Record<string, SkillCommand> = {
  "yazhi-start": { skill: "yazhi-work-start" },
  "yazhi-purpose": { skill: "yazhi-purpose-gate" },
  "yazhi-review": { skill: "yazhi-review" },
  "yazhi-issue": { skill: "yazhi-code-writeup", mode: "issue" },
  "yazhi-pr": { skill: "yazhi-code-writeup", mode: "pr" },
};

const DANGEROUS_BASH = [
  /\brm\s+(-rf?|--recursive)\b/i,
  /\bsudo\b/i,
  /\bgit\s+push\b.*--force(?:-with-lease)?\b/i,
  /\b(chmod|chown)\b.*777\b/i,
  /\b(shutdown|reboot|mkfs)\b/i,
];

const PROTECTED_PATHS = [
  ".env",
  ".git/",
  "node_modules/",
  ".ssh/",
  "id_rsa",
  "credentials",
];

function dangerousReason(command: string): string | undefined {
  const match = DANGEROUS_BASH.find((pattern) => pattern.test(command));
  return match ? `Dangerous command matched /${match.source}/` : undefined;
}

function protectedReason(path: string): string | undefined {
  const match = PROTECTED_PATHS.find((fragment) => path.includes(fragment));
  return match ? `Protected path fragment "${match}"` : undefined;
}

export default function yazhiExtension(pi: ExtensionAPI) {
  for (const [name, command] of Object.entries(SKILL_COMMANDS)) {
    pi.registerCommand(name, {
      description: `Queue /skill:${command.skill}${command.mode ? ` (${command.mode} mode)` : ""} from the yazhi-skills collection`,
      handler: async (args, ctx) => {
        if (!ctx.hasUI) {
          ctx.ui.notify(`${name} needs interactive mode to queue a skill`, "error");
          return;
        }
        const suffix = [command.mode, args.trim()].filter(Boolean).join(" ");
        ctx.ui.setEditorText(`/skill:${command.skill}${suffix ? ` ${suffix}` : ""}`);
        ctx.ui.notify(`${command.skill} queued — submit to load it`, "info");
      },
    });
  }

  pi.on("tool_call", async (event, ctx) => {
    if (isToolCallEventType("bash", event)) {
      const reason = dangerousReason(event.input.command);
      if (reason) {
        if (!ctx.hasUI) {
          return { block: true, reason: `Yazhi guard: ${reason} (no UI to confirm)` };
        }
        const allowed = await ctx.ui.confirm(
          "Yazhi safety gate",
          `${reason}\n\n${event.input.command}\n\nAllow this command?`,
        );
        if (!allowed) return { block: true, reason: "Blocked by Yazhi safety gate" };
      }
    }

    if (event.toolName === "write" || event.toolName === "edit") {
      const path = String(event.input.path ?? "");
      const reason = protectedReason(path);
      if (reason) {
        if (ctx.hasUI) ctx.ui.notify(`Yazhi guard blocked ${path}: ${reason}`, "warning");
        return { block: true, reason: `Yazhi guard: ${reason}` };
      }
    }

    return undefined;
  });

  async function guardDirtyRepo(
    ctx: ExtensionContext,
  ): Promise<{ cancel: boolean } | undefined> {
    const result = await pi.exec("git", ["status", "--porcelain"]);
    if (result.code !== 0 || !result.stdout.trim()) return undefined;

    const files = result.stdout.trim().split("\n").length;
    const message = `You have ${files} uncommitted file(s). Commit or hand off before leaving this session.`;
    if (!ctx.hasUI) return { cancel: true };

    const proceed = await ctx.ui.confirm("Yazhi checkpoint guard", `${message}\n\nContinue anyway?`);
    return proceed ? undefined : { cancel: true };
  }

  pi.on("session_before_switch", async (_event, ctx) => guardDirtyRepo(ctx));
  pi.on("session_before_fork", async (_event, ctx) => guardDirtyRepo(ctx));
}
