export default function handler(req, res) {
  console.log(JSON.stringify({
    event: 'execute_blocked',
    productionConnected: false
  }));
  res.status(503).json({
    ok: false,
    error: 'production_execution_disabled',
    productionConnected: false,
    message: 'This independent Agent Lab Edge cannot execute MACH production services.'
  });
}
