// graphify OpenCode plugin
// On-demand knowledge graph queries. Does NOT add noise to bash calls.
// Use via /graphify query when you need cross-cutting analysis.
import { existsSync } from "fs";
import { join } from "path";

export const GraphifyPlugin = async ({ directory }) => {
  const graphPath = join(directory, "graphify-out", "graph.json");
  const hasGraph = existsSync(graphPath);

  return {
    // No automatic injection - the graph is an on-demand tool.
    // To query: use the /graphify skill at the conversation level.
    "tool.execute.before": async (input, output) => {
      // Silent pass-through - graphify is purely on-demand
    },
  };
};
