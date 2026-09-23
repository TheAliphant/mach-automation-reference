export default function handler(req, res) {
  res.status(200).json({
    status: 'ok',
    mode: 'lab_only',
    productionConnected: false,
    a2a: {
      protocolVersion: '1.0',
      binding: 'HTTP+JSON',
      sendMessage: true,
      streaming: false,
      productionExecution: false
    }
  });
}
