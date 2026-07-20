import React, { useState, useEffect } from 'react';
import CognitiveOrb from './CognitiveOrb';

export default function App() {
  const [aiState, setAiState] = useState('LISTENING');
  const [metrics, setMetrics] = useState(null);

  // เชื่อมต่อ WebSocket กับ Backend ของคุณ
  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/telemetry');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data);
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{ background: '#0a0b10', color: '#00f3ff', minHeight: '100vh', padding: '20px', fontFamily: 'monospace' }}>
      <h1>ONE OS - MISSION CONTROL</h1>
      <p>KERNEL STATE: {metrics ? metrics.kernel_state : 'CONNECTING...'}</p>

      {/* กล่องแสดงผล 3D Cognitive Orb */}
      <div style={{ width: '450px', height: '450px', margin: '20px auto', border: '1px solid rgba(0,243,255,0.3)', borderRadius: '10px' }}>
        <CognitiveOrb state={aiState} />
      </div>

      {/* แผงควบคุมจำลองสถานะ Orb */}
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
        <button onClick={() => setAiState('LISTENING')}>Listening (Cyan)</button>
        <button onClick={() => setAiState('THINKING')}>Thinking (Purple)</button>
        <button onClick={() => setAiState('SPEAKING')}>Speaking (Green)</button>
        <button onClick={() => setAiState('ALERT')}>Alert (Red)</button>
      </div>
    </div>
  );
}