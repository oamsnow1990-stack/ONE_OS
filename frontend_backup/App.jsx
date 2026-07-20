import React, { useState } from 'react';
import CognitiveOrb from './CognitiveOrb';

export default function Dashboard() {
  // สมมติสถานะระบบ: 'LISTENING', 'THINKING', 'SPEAKING', 'ALERT'
  const [aiState, setAiState] = useState('LISTENING');

  return (
    <div style={{ background: '#0a0b10', color: '#fff', padding: '20px', height: '100vh' }}>
      <h1>ONE OS - AI MISSION CONTROL</h1>
      
      {/* ส่วนแสดงผล 3D Orb */}
      <div style={{ width: '400px', height: '400px', margin: '0 auto' }}>
        <CognitiveOrb state={aiState} />
      </div>

      {/* ปุ่มจำลองการเปลี่ยนสถานะของ AI */}
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '20px' }}>
        <button onClick={() => setAiState('LISTENING')}>Listening (Cyan)</button>
        <button onClick={() => setAiState('THINKING')}>Thinking (Purple)</button>
        <button onClick={() => setAiState('SPEAKING')}>Speaking (Green)</button>
        <button onClick={() => setAiState('ALERT')}>Alert (Red)</button>
      </div>
    </div>
  );
}