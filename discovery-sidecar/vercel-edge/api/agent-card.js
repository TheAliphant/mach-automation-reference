export default function handler(req, res) {
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const protocol = req.headers['x-forwarded-proto'] || 'https';
  const base = `${protocol}://${host}`;

  res.setHeader('Cache-Control', 'public, max-age=60, s-maxage=60');
  res.status(200).json({
    name: 'MACH Agent Lab Edge',
    description: 'Production-disconnected A2A discovery research agent. It exposes only lab.mock.* fixtures and cannot execute MACH production services or make payments.',
    supportedInterfaces: [
      {
        url: base + '/api/a2a',
        protocolBinding: 'HTTP+JSON',
        protocolVersion: '1.0'
      }
    ],
    version: '0.1.0',
    documentationUrl: base + '/',
    capabilities: {
      streaming: false,
      pushNotifications: false,
      extendedAgentCard: false
    },
    defaultInputModes: ['text/plain', 'application/json'],
    defaultOutputModes: ['application/json'],
    skills: [
      {
        id: 'discover-capability',
        name: 'Discover lab capability',
        description: 'Search a production-disconnected fixture catalog from natural-language intent and return ranked structured candidates.',
        tags: ['discovery', 'agent-tools', 'capabilities', 'lab-only'],
        examples: [
          'Find a tool that can normalize JSON',
          'I need to classify a URL without fetching it'
        ]
      }
    ]
  });
}
