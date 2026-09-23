import { discover, extractMessageText, makeId } from './_lib/capabilities.js';

export default function handler(req, res) {
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: {
        code: 405,
        message: 'method_not_allowed'
      }
    });
  }

  const request = req.body && typeof req.body === 'object' ? req.body : {};
  const message = request.message && typeof request.message === 'object' ? request.message : {};

  if (
    typeof message.messageId !== 'string' ||
    message.role !== 'ROLE_USER' ||
    !Array.isArray(message.parts) ||
    message.parts.length === 0
  ) {
    return res.status(400).json({
      error: {
        code: 400,
        message: 'invalid_a2a_message',
        details: 'A2A v1.0 Message requires messageId, ROLE_USER and at least one Part.'
      }
    });
  }

  const query = extractMessageText(message);
  if (!query) {
    return res.status(400).json({
      error: {
        code: 400,
        message: 'empty_a2a_message',
        details: 'Provide a text Part or a data Part containing task, query or intent.'
      }
    });
  }

  const results = discover(query);
  const contextId = typeof message.contextId === 'string' && message.contextId
    ? message.contextId
    : makeId('ctx');

  console.log(JSON.stringify({
    event: 'a2a_message',
    messageId: message.messageId,
    contextId,
    query,
    resultCount: results.length,
    productionConnected: false
  }));

  return res.status(200).json({
    message: {
      messageId: makeId('msg'),
      contextId,
      role: 'ROLE_AGENT',
      parts: [
        {
          data: {
            mode: 'lab_only',
            productionConnected: false,
            query,
            results,
            note: 'Discovery research only. MACH production is not connected.'
          },
          mediaType: 'application/json'
        }
      ],
      metadata: {
        a2aProtocolVersion: '1.0',
        labOnly: true
      }
    }
  });
}
