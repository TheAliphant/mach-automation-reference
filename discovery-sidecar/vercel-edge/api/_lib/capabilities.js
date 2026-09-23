export const CAPABILITIES = [
  {
    id: 'lab.mock.json-normalize',
    name: 'Normalize JSON',
    tags: ['json', 'normalize', 'validate', 'structure'],
    description: 'Normalize a JSON object into a stable deterministic key order for agent discovery testing.',
    inputSchema: {
      type: 'object',
      properties: { value: { type: 'object' } },
      required: ['value']
    },
    outputSchema: {
      type: 'object',
      properties: { normalized: { type: 'object' } },
      required: ['normalized']
    },
    priceUsd: 0,
    typicalLatencyMs: 5
  },
  {
    id: 'lab.mock.url-classify',
    name: 'Classify URL intent',
    tags: ['url', 'classify', 'intent', 'routing'],
    description: 'Classify a URL string locally without fetching it.',
    inputSchema: {
      type: 'object',
      properties: { url: { type: 'string' } },
      required: ['url']
    },
    outputSchema: {
      type: 'object',
      properties: { category: { type: 'string' } },
      required: ['category']
    },
    priceUsd: 0,
    typicalLatencyMs: 5
  },
  {
    id: 'lab.mock.wallet-format',
    name: 'Validate wallet-address format',
    tags: ['wallet', 'address', 'validate', 'format'],
    description: 'Validate only the local string format of an EVM-style address. No blockchain lookup is performed.',
    inputSchema: {
      type: 'object',
      properties: { address: { type: 'string' } },
      required: ['address']
    },
    outputSchema: {
      type: 'object',
      properties: { validFormat: { type: 'boolean' } },
      required: ['validFormat']
    },
    priceUsd: 0,
    typicalLatencyMs: 5
  }
];

function tokens(text = '') {
  return new Set(String(text).toLowerCase().split(/[^a-z0-9_]+/).filter(token => token.length > 1));
}

export function discover(query) {
  const wanted = tokens(query);
  return CAPABILITIES
    .map(capability => {
      const haystack = tokens([
        capability.id,
        capability.name,
        capability.description,
        ...capability.tags
      ].join(' '));
      const score = [...wanted].filter(word => haystack.has(word)).length;
      return {
        id: capability.id,
        name: capability.name,
        description: capability.description,
        score,
        priceUsd: capability.priceUsd,
        typicalLatencyMs: capability.typicalLatencyMs,
        status: 'lab_only'
      };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id))
    .slice(0, 5);
}

export function extractMessageText(message = {}) {
  const parts = Array.isArray(message.parts) ? message.parts : [];
  return parts
    .map(part => {
      if (part && typeof part.text === 'string') return part.text;
      const data = part && typeof part.data === 'object' && part.data ? part.data : {};
      return [data.task, data.query, data.intent].filter(value => typeof value === 'string').join(' ');
    })
    .filter(Boolean)
    .join(' ')
    .slice(0, 1500);
}

export function makeId(prefix) {
  return prefix + '-' + Date.now().toString(36) + '-' + Math.random().toString(16).slice(2, 10);
}
