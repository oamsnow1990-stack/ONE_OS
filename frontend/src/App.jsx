import React, { useState, useEffect } from 'react';

export default function App() {
  const [activeTab, setActiveTab] = useState('COGNITIVE_TRACE');
  const [aiState, setState] = useState('REASONING');
  
  // 3. Live World State
  const [worldState, setWorldState] = useState({
    weather: 'Storm',
    threat: '87%',
    mission: 'Explore & Secure',
    target: 'Zone-4'
  });

  // 1. Explainable Cognition & Step State
  const [cognitiveStep, setCognitiveStep] = useState(2); // 0: Obs, 1: Pattern, 2: Recall, 3: Sim, 4: Decision, 5: Reason
  const stepsList = ['Observation', 'Pattern Analysis', 'Memory Recall', 'Simulation', 'Decision', 'Reason'];

  // 2. Evidence Panel Data
  const [evidence, setEvidence] = useState({
    episode: 'Episode #241',
    confidence: '91%',
    reason: 'Resource shortage & high electromagnetic interference',
    weatherImpact: 'Critical'
  });

  // 5. Interactive "WHY?" State
  const [whyModalOpen, setWhyModalOpen] = useState(false);
  const [whyDetails, setWhyDetails] = useState({
    probability: '91.4%',
    memoryMatch: '83.2%',
    expectedSuccess: '72.0%',
    decisionMode: 'SAFE MODE'
  });

  // Engine Loads (Reasoning, Memory, Planning, Execution)
  const [engines, setEngines] = useState({
    reasoning: 92,
    memory: 88,
    planning: 79,
    execution: 85
  });

  // 6. Cognitive Timeline (Flight Recorder)
  const [flightRecorder, setFlightRecorder] = useState([
    { time: '14:10:31', event: 'Observe', detail: 'Telemetry stream ingested from Zone-4' },
    { time: '14:10:32', event: 'Recall', detail: 'Pulled Episode #241 (Storm mitigation)' },
    { time: '14:10:33', event: 'Simulate', detail: 'Branching test indicates 72% success' },
    { time: '14:10:34', event: 'Choose', detail: 'Engaging Safe Mode override' },
    { time: '14:10:35', event: 'Execute', detail: 'Vector dispatch locked' }
  ]);

  // Simulation loop สำหรับขยับขั้นตอนการคิดและอัปเดต Timeline
  useEffect(() => {
    const interval = setInterval(() => {
      setCognitiveStep(prev => {
        const nextStep = (prev + 1) % stepsList.length;
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        
        // บันทึกเข้า Flight Recorder ทุกครั้งที่เปลี่ยนสเต็ป
        setFlightRecorder(old => [
          { time: timeStr, event: stepsList[nextStep], detail: `Processed active node telemetry for ${stepsList[nextStep]}` },
          ...old.slice(0, 15)
        ]);

        return nextStep;
      });
    }, 4500);
    return () => clearInterval(interval);
  }, []);

  const colors = {
    bg: '#020408',
    glass: 'rgba(8, 14, 26, 0.95)',
    primary: '#00F6FF',
    purple: '#8E4DFF',
    green: '#00FF88',
    warning: '#FFC84A',
    danger: '#FF4E5B',
    textMuted: '#6B7C93'
  };

  return (
    <div style={{
      background: colors.bg, color: '#fff', minHeight: '100vh',
      fontFamily: "'Courier New', Courier, monospace",
      display: 'grid', gridTemplateColumns: '240px 1fr 300px', gridTemplateRows: '80px 1fr 140px',
      gridTemplateAreas: `"sidebar header header" "sidebar main rightpanel" "sidebar timeline timeline"`,
      overflow: 'hidden', position: 'relative', userSelect: 'none'
    }}>
      <style>{`
        .glass-box { background: ${colors.glass}; backdrop-filter: blur(16px); border: 1px solid ${colors.primary}30; border-radius: 6px; padding: 12px; }
        .step-pill { padding: 6px 12px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; transition: all 0.3s; }
        .why-btn { background: linear-gradient(135deg, ${colors.purple}, ${colors.primary}); border: none; color: #fff; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-family: inherit; font-weight: bold; font-size: 0.75rem; letter-spacing: 1px; box-shadow: 0 0 15px ${colors.purple}60; transition: transform 0.2s; }
        .why-btn:hover { transform: scale(1.05); }
        .timeline-row { display: flex; align-items: center; gap: 15px; padding: 6px 10px; border-left: 2px solid ${colors.primary}; background: rgba(0,246,255,0.03); margin-bottom: 6px; border-radius: 0 4px 4px 0; font-size: 0.65rem; }
      `}</style>

      {/* Sidebar: Navigation OS */}
      <div style={{ gridArea: 'sidebar', background: '#010204', borderRight: '1px solid rgba(0,246,255,0.1)', display: 'flex', flexDirection: 'column', padding: '15px', zIndex: 20 }}>
         <h2 style={{ color: colors.primary, fontSize: '0.85rem', letterSpacing: '3px', marginBottom: '20px' }}>ONE OS v10.0</h2>
         <div style={{ fontSize: '0.6rem', color: colors.textMuted, marginBottom: '10px', letterSpacing: '1px' }}>SYSTEM MODULES</div>
         {['COGNITIVE TRACE', 'WORLD TELEMETRY', 'FLIGHT RECORDER', 'ENGINE KERNEL'].map(tab => (
            <div key={tab} onClick={() => setActiveTab(tab)} style={{ padding: '10px 12px', cursor: 'pointer', color: activeTab === tab ? colors.primary : colors.textMuted, fontSize: '0.75rem', background: activeTab === tab ? `${colors.primary}15` : 'transparent', borderRadius: '4px', marginBottom: '4px' }}>
              {activeTab === tab ? '▶ ' : '  '} {tab}
            </div>
         ))}
      </div>

      {/* Header: Live World State & System Status */}
      <div style={{ gridArea: 'header', borderBottom: '1px solid rgba(0,246,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px', background: '#010204', zIndex: 20, fontSize: '0.65rem' }}>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div><span style={{ color: colors.textMuted }}>WORLD:</span> <span style={{ color: colors.warning, fontWeight: 'bold' }}>{worldState.weather}</span></div>
          <div><span style={{ color: colors.textMuted }}>THREAT:</span> <span style={{ color: colors.danger, fontWeight: 'bold' }}>{worldState.threat}</span></div>
          <div><span style={{ color: colors.textMuted }}>MISSION:</span> <span style={{ color: '#fff' }}>{worldState.mission}</span></div>
          <div><span style={{ color: colors.textMuted }}>TARGET:</span> <span style={{ color: colors.primary }}>{worldState.target}</span></div>
        </div>
        <div style={{ background: 'rgba(0,255,136,0.1)', border: '1px solid #00FF8840', padding: '4px 10px', borderRadius: '4px', color: colors.green, fontWeight: 'bold' }}>
          COG-OS: ONLINE
        </div>
      </div>

      {/* Main Center: Explainable Cognition & Central Hub */}
      <div style={{ gridArea: 'main', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative', padding: '20px', zIndex: 20, gap: '20px' }}>
        
        {/* 1. Explainable Cognition Pipeline */}
        <div className="glass-box" style={{ width: '90%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(3,7,14,0.9)' }}>
          {stepsList.map((stepName, idx) => {
            const isActive = cognitiveStep === idx;
            return (
              <div key={stepName} className="step-pill" style={{
                background: isActive ? colors.primary : 'rgba(255,255,255,0.03)',
                color: isActive ? '#000' : colors.textMuted,
                border: `1px solid ${isActive ? colors.primary : 'rgba(255,255,255,0.1)'}`,
                boxShadow: isActive ? `0 0 15px ${colors.primary}80` : 'none'
              }}>
                {idx + 1}. {stepName.toUpperCase()}
              </div>
            );
          })}
        </div>

        {/* Central Visualization & Interactive WHY? Trigger */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '15px' }}>
          <div style={{ 
            width: '180px', height: '180px', borderRadius: '50%', border: `2px solid ${colors.primary}`, 
            boxShadow: `0 0 50px ${colors.primary}50 inset, 0 0 25px ${colors.primary}30`,
            display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative'
          }}>
            <div style={{ fontSize: '0.6rem', color: colors.textMuted, letterSpacing: '2px' }}>ACTIVE COGNITION</div>
            <div style={{ fontSize: '0.9rem', color: colors.primary, fontWeight: 'bold', marginTop: '5px' }}>{stepsList[cognitiveStep].toUpperCase()}</div>
            <div style={{ fontSize: '0.55rem', color: colors.green, marginTop: '5px' }}>● KERNEL SYNCED</div>
          </div>

          {/* 5. Explain Button ("WHY?") */}
          <button className="why-btn" onClick={() => setWhyModalOpen(!whyModalOpen)}>
            {whyModalOpen ? '[ CLOSE DIAGNOSTIC ]' : '⚡ WHY THIS DECISION?'}
          </button>
        </div>

        {/* Diagnostic Modal Popup when WHY is clicked */}
        {whyModalOpen && (
          <div className="glass-box" style={{ width: '70%', background: 'rgba(10,5,20,0.95)', border: `1px solid ${colors.purple}`, position: 'absolute', top: '15%', zIndex: 100, padding: '20px' }}>
            <div style={{ color: colors.purple, fontWeight: 'bold', fontSize: '0.8rem', marginBottom: '10px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '5px' }}>
              🧠 COGNITIVE DIAGNOSTIC RATIONALE (WHY?)
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', fontSize: '0.7rem', textAlign: 'center' }}>
              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '4px' }}>
                <div style={{ color: colors.textMuted, fontSize: '0.6rem' }}>PROBABILITY</div>
                <div style={{ color: colors.primary, fontWeight: 'bold', fontSize: '0.9rem' }}>{whyDetails.probability}</div>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '4px' }}>
                <div style={{ color: colors.textMuted, fontSize: '0.6rem' }}>MEMORY MATCH</div>
                <div style={{ color: colors.green, fontWeight: 'bold', fontSize: '0.9rem' }}>{whyDetails.memoryMatch}</div>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '4px' }}>
                <div style={{ color: colors.textMuted, fontSize: '0.6rem' }}>EXP. SUCCESS</div>
                <div style={{ color: colors.warning, fontWeight: 'bold', fontSize: '0.9rem' }}>{whyDetails.expectedSuccess}</div>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '4px' }}>
                <div style={{ color: colors.textMuted, fontSize: '0.6rem' }}>DECISION MODE</div>
                <div style={{ color: colors.danger, fontWeight: 'bold', fontSize: '0.9rem' }}>{whyDetails.decisionMode}</div>
              </div>
            </div>
            <div style={{ marginTop: '12px', fontSize: '0.65rem', color: colors.textMuted, fontStyle: 'italic' }}>
              * Derived from multi-engine convergence. External environmental threat (Storm) prioritized over standard route execution.
            </div>
          </div>
        )}

      </div>

      {/* Right Panel: 2. Evidence Panel & Engine Kernels */}
      <div style={{ gridArea: 'rightpanel', padding: '15px', display: 'flex', flexDirection: 'column', gap: '12px', zIndex: 20 }}>
        
        {/* Evidence Panel */}
        <div className="glass-box" style={{ fontSize: '0.65rem' }}>
          <div style={{ color: colors.warning, marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '3px', fontWeight: 'bold' }}>
            📂 EVIDENCE PANEL
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
            <span style={{ color: colors.textMuted }}>Reference:</span><span style={{ color: '#fff', fontWeight: 'bold' }}>{evidence.episode}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
            <span style={{ color: colors.textMuted }}>Confidence:</span><span style={{ color: colors.green, fontWeight: 'bold' }}>{evidence.confidence}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
            <span style={{ color: colors.textMuted }}>Weather Factor:</span><span style={{ color: colors.danger }}>{evidence.weatherImpact}</span>
          </div>
          <div style={{ marginTop: '6px', color: colors.textMuted, fontSize: '0.6rem' }}>
            <strong>Primary Reason:</strong> {evidence.reason}
          </div>
        </div>

        {/* 4. Real Backend Engine Loads */}
        <div className="glass-box" style={{ fontSize: '0.65rem', flex: 1 }}>
          <div style={{ color: colors.primary, marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '3px', fontWeight: 'bold' }}>
            ⚙️ ENGINE KERNEL LOADS
          </div>
          {Object.entries(engines).map(([engineName, loadVal]) => (
            <div key={engineName} style={{ marginBottom: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px', textTransform: 'uppercase' }}>
                <span style={{ color: colors.textMuted }}>{engineName} Engine</span>
                <span style={{ color: colors.primary }}>{loadVal}%</span>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', height: '2px', borderRadius: '2px', overflow: 'hidden' }}>
                <div style={{ width: `${loadVal}%`, height: '100%', background: colors.primary }} />
              </div>
            </div>
          ))}
        </div>

      </div>

      {/* Bottom Bar: 6. Cognitive Timeline (Flight Recorder) */}
      <div style={{ gridArea: 'timeline', display: 'flex', flexDirection: 'column', padding: '10px 15px', background: '#010204', borderTop: '1px solid rgba(0,246,255,0.1)', zIndex: 20, overflow: 'hidden' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.65rem', color: colors.primary, letterSpacing: '2px', marginBottom: '6px' }}>
          <span>FLIGHT RECORDER (COGNITIVE TIMELINE)</span>
          <span style={{ color: colors.textMuted }}>* Real-time event log buffer</span>
        </div>
        <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '5px' }}>
          {flightRecorder.map((rec, idx) => (
            <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '4px', padding: '6px 10px', minWidth: '160px', flexShrink: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.55rem', color: colors.warning, marginBottom: '2px' }}>
                <span>[{rec.time}]</span><span style={{ color: colors.primary, fontWeight: 'bold' }}>{rec.event}</span>
              </div>
              <div style={{ fontSize: '0.6rem', color: '#fff', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {rec.detail}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}