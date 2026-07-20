import React, { useState, useEffect } from 'react';

export default function App() {
  const [activeTab, setActiveTab] = useState('EXECUTIVE_CORE');
  const [aiState, setAiState] = useState('EXECUTING');
  
  // Executive Mission & Priority Manager State
  const [missions, setMissions] = useState([
    { id: 'M-1', name: 'EXPLORE_ENVIRONMENT', priority: 'HIGH', status: 'ACTIVE', progress: 84 },
    { id: 'M-2', name: 'RESOLVE_CONFLICT', priority: 'CRITICAL', status: 'QUEUED', progress: 12 },
    { id: 'M-3', name: 'LONG_TERM_PLANNING', priority: 'NORMAL', status: 'STANDBY', progress: 45 }
  ]);

  const [cognitive, setCognitive] = useState({
    intent: 'EXECUTING', level: 94, state: 'Hyper Focus', mood: 'Focused',
    mission: 'EXPLORE_ENVIRONMENT', objective: 'Pattern Recognition', task: 'Execute Priority Queue Routing',
    reflection: 'Mission switching criteria met. Re-allocating core resources to high-priority objectives.'
  });

  const [reasoning, setReasoning] = useState({
    why: "Executive override: Prioritizing environment exploration while maintaining conflict resolution background queue.",
    evidence: [{ id: 'EV-PR', label: 'Priority Weight', value: '0.94' }, { id: 'EV-Q', label: 'Queue Depth', value: '3 Tasks' }],
    memory: [{ id: 'MEM-EX', label: 'Executive Routine', match: '99%' }]
  });

  const [kernelStats, setKernelStats] = useState({
    eegFreq: 32, eegWave: 'BETA', latency: 3.1, tps: 92.1, packetsPerSec: 450,
    sync: 99.9, ws: 'ONLINE', ping: '1ms', uptime: '06:14:02'
  });

  const [pipeline, setPipeline] = useState({ capture: 10, analysis: 25, memory: 15, decision: 20, action: 5, total: 75 });
  
  const [engines, setEngines] = useState([
    { id: 'reasoning', name: 'REASONING', symbol: '◆', color: '#8E4DFF', load: 95, side: 'left' },
    { id: 'planning', name: 'PLANNING', symbol: '●', color: '#00F6FF', load: 91, side: 'left' },
    { id: 'learning', name: 'LEARNING', symbol: '✦', color: '#00FF88', load: 88, side: 'left' },
    { id: 'memory', name: 'MEMORY', symbol: '○', color: '#00FF88', load: 90, side: 'left' },
    { id: 'simulation', name: 'SIMULATION', symbol: '◇', color: '#00F6FF', load: 85, side: 'right' },
    { id: 'validator', name: 'VALIDATOR', symbol: '■', color: '#FFC84A', load: 94, side: 'right' },
    { id: 'reflection', name: 'REFLECTION', symbol: '◈', color: '#FFC84A', load: 82, side: 'right' },
    { id: 'execution', name: 'EXECUTION', symbol: '▶', color: '#00FF88', load: 98, side: 'right' },
  ]);

  const [packets, setPackets] = useState([]);
  const [dustLayers, setDustLayers] = useState({ bg: [], mid: [], fg: [] });
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Neural Dust Generation (Optimized once on mount)
  useEffect(() => {
    const createDust = (count, sizeMin, sizeMax, opacityMin, opacityMax) => 
      Array.from({ length: count }).map(() => ({
        x: Math.random() * 100, y: Math.random() * 100,
        size: Math.random() * (sizeMax - sizeMin) + sizeMin,
        opacity: Math.random() * (opacityMax - opacityMin) + opacityMin,
        speedMod: Math.random() * 1.5 + 0.5
      }));
    setDustLayers({
      bg: createDust(120, 0.5, 1, 0.05, 0.15),
      mid: createDust(80, 1, 2, 0.15, 0.3),
      fg: createDust(20, 2, 3.5, 0.4, 0.7)
    });
    const handleMouseMove = (e) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20
      });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Executive Goal Switching Cycle (Stable Timers)
  useEffect(() => {
    let step = 0;
    const cycle = setInterval(() => {
      step = (step + 1) % 3;
      switch(step) {
        case 0:
          setAiState('EXECUTING');
          setCognitive({ intent: 'EXECUTING', level: 94, state: 'Hyper Focus', mood: 'Focused', mission: 'EXPLORE_ENVIRONMENT', objective: 'Pattern Recognition', task: 'Execute Priority Queue Routing', reflection: 'Mission switching criteria met. Allocating resources to M-1.' });
          setMissions([
            { id: 'M-1', name: 'EXPLORE_ENVIRONMENT', priority: 'HIGH', status: 'ACTIVE', progress: 91 },
            { id: 'M-2', name: 'RESOLVE_CONFLICT', priority: 'CRITICAL', status: 'QUEUED', progress: 24 },
            { id: 'M-3', name: 'LONG_TERM_PLANNING', priority: 'NORMAL', status: 'STANDBY', progress: 50 }
          ]);
          setReasoning({ why: "Executive scheduler maintains M-1 as primary active mission.", evidence: [{ id: 'EV-PR', label: 'Weight', value: '0.94' }], memory: [{ id: 'MEM-EX', label: 'Routine M-1', match: '99%' }] });
          break;
        case 1:
          setAiState('DECIDING');
          setCognitive({ intent: 'DECIDING', level: 99, state: 'Emergency', mood: 'Danger', mission: 'RESOLVE_CONFLICT', objective: 'Safety Override', task: 'Re-prioritize queue for emergency protocol', reflection: 'CRITICAL EVENT: Mission Switch triggered. Elevating M-2 to Active State.' });
          setMissions([
            { id: 'M-1', name: 'EXPLORE_ENVIRONMENT', priority: 'HIGH', status: 'PAUSED', progress: 91 },
            { id: 'M-2', name: 'RESOLVE_CONFLICT', priority: 'CRITICAL', status: 'ACTIVE', progress: 68 },
            { id: 'M-3', name: 'LONG_TERM_PLANNING', priority: 'NORMAL', status: 'STANDBY', progress: 50 }
          ]);
          setReasoning({ why: "Emergency priority override executed. Shifting focus to conflict resolution.", evidence: [{ id: 'EV-EM', label: 'Threat Level', value: 'Critical' }], memory: [{ id: 'MEM-OC', label: 'Override Code', match: '100%' }] });
          break;
        case 2:
          setAiState('PREDICTING');
          setCognitive({ intent: 'PREDICTING', level: 90, state: 'Dreaming', mood: 'Creative', mission: 'LONG_TERM_PLANNING', objective: 'Macro Horizon Forecast', task: 'Simulate next 24h operational state', reflection: 'System stable. Shifting executive focus to long-term architectural projections.' });
          setMissions([
            { id: 'M-1', name: 'EXPLORE_ENVIRONMENT', priority: 'HIGH', status: 'COMPLETED', progress: 100 },
            { id: 'M-2', name: 'RESOLVE_CONFLICT', priority: 'CRITICAL', status: 'COMPLETED', progress: 100 },
            { id: 'M-3', name: 'LONG_TERM_PLANNING', priority: 'NORMAL', status: 'ACTIVE', progress: 85 }
          ]);
          setReasoning({ why: "Tactical goals achieved. Engaging long-term macro simulation routine.", evidence: [{ id: 'EV-LT', label: 'Horizon', value: '24h' }], memory: [{ id: 'MEM-LT', label: 'Strategic Plan', match: '94%' }] });
          break;
      }
    }, 6000); 
    return () => clearInterval(cycle);
  }, []);

  // Update Engines and Smooth Packet Stream
  useEffect(() => {
    const interval = setInterval(() => {
      setKernelStats(prev => ({
        ...prev,
        tps: parseFloat((90 + (Math.random() - 0.5) * 3).toFixed(1)),
        latency: parseFloat((3.1 + (Math.random() - 0.5) * 0.1).toFixed(1)),
        packetsPerSec: 450 + Math.floor((Math.random() - 0.5) * 20)
      }));

      setEngines(prev => prev.map(e => ({
        ...e,
        load: Math.min(99, Math.max(40, e.load + Math.floor(Math.random() * 6) - 3))
      })));

      const randomEngine = engines[Math.floor(Math.random() * engines.length)];
      setPackets(prev => [...prev.slice(-20), {
        id: Date.now() + Math.random(), color: randomEngine.color, side: randomEngine.side, progress: 0,
        speed: 0.015, history: [] 
      }]);
    }, 700);
    return () => clearInterval(interval);
  }, [engines]);

  // Smooth Animation Loop for Packets & Temporal Echoes
  useEffect(() => {
    const animInterval = setInterval(() => {
      setPackets(prev => prev.map(p => {
        const newHistory = [p.progress, ...p.history].slice(0, 3);
        return { ...p, progress: p.progress + p.speed, history: newHistory };
      }).filter(p => p.progress < 1));
    }, 30);
    return () => clearInterval(animInterval);
  }, []);

  const colors = { bg: '#010204', glass: 'rgba(6, 10, 18, 0.95)', primary: '#00F6FF', purple: '#8E4DFF', green: '#00FF88', warning: '#FFC84A', danger: '#FF4E5B', textMuted: '#7D8DA1' };
  const getMoodColor = () => {
    switch(cognitive.mood) {
      case 'Curious': return colors.purple;
      case 'Danger': return colors.danger;
      case 'Creative': return colors.warning;
      case 'Focused': return colors.primary;
      default: return colors.primary;
    }
  };

  const getPacketPos = (side, progress) => {
    const startX = side === 'left' ? 20 : window.innerWidth - 560;
    const endX = (window.innerWidth - 520) / 2;
    const centerY = window.innerHeight / 2 - 120;
    return { x: startX + (endX - startX) * progress, y: centerY + (progress - 0.5) * 80 };
  };

  return (
    <div style={{
      background: colors.bg, color: '#fff', minHeight: '100vh', fontFamily: "'Courier New', Courier, monospace",
      display: 'grid', gridTemplateColumns: '240px 1fr 280px', gridTemplateRows: '85px 1fr 100px',
      gridTemplateAreas: `"sidebar header header" "sidebar main rightpanel" "sidebar timeline timeline"`,
      overflow: 'hidden', position: 'relative', userSelect: 'none'
    }}>
      <style>{`
        @keyframes coreExec { 0%, 100% { transform: scale(1); filter: drop-shadow(0 0 25px ${getMoodColor()}); } 50% { transform: scale(1.03); filter: drop-shadow(0 0 45px ${getMoodColor()}); } }
        @keyframes spinMesh { 100% { transform: rotate(360deg); } }
        @keyframes spinMeshReverse { 100% { transform: rotate(-360deg); } }
        @keyframes dustFloat { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-12px); } }
        .core-state { animation: coreExec 2.2s infinite ease-in-out; will-change: transform, filter; }
        .glass-box { background: ${colors.glass}; backdrop-filter: blur(16px); border: 1px solid ${getMoodColor()}40; border-radius: 8px; padding: 10px; transition: border-color 0.5s ease; }
        .stat-value { color: #fff; font-weight: bold; }
        .stat-label { color: ${colors.textMuted}; margin-right: 4px; }
      `}</style>

      {/* Neural Dust Background */}
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh', pointerEvents: 'none', zIndex: 1, overflow: 'hidden' }}>
        {dustLayers.bg.map((d, i) => (
            <div key={`bg-${i}`} style={{
              position: 'absolute', left: `${d.x}%`, top: `${d.y}%`, width: `${d.size}px`, height: `${d.size}px`, 
              background: '#fff', borderRadius: '50%', opacity: d.opacity,
              transform: `translate(${mousePos.x * 0.2}px, ${mousePos.y * 0.2}px)`,
              animation: `dustFloat ${15 + d.speedMod * 10}s infinite ease-in-out`
            }} />
        ))}
      </div>

      {/* Temporal Echo Packets */}
      <svg style={{ position: 'absolute', top: 85, left: 240, width: 'calc(100vw - 520px)', height: 'calc(100vh - 185px)', pointerEvents: 'none', zIndex: 10 }}>
        {packets.map(p => {
          const currentPos = getPacketPos(p.side, p.progress);
          return (
            <g key={p.id}>
              {p.history && p.history.map((histProg, idx) => {
                const histPos = getPacketPos(p.side, histProg);
                return <circle key={`${p.id}-hist-${idx}`} cx={histPos.x} cy={histPos.y} r={3 - (idx * 0.8)} fill={p.color} opacity={0.3 - (idx * 0.1)} style={{ filter: `blur(1px)` }} />;
              })}
              <circle cx={currentPos.x} cy={currentPos.y} r="3.5" fill={p.color} style={{ filter: `drop-shadow(0 0 8px ${p.color})` }} />
            </g>
          );
        })}
      </svg>

      {/* Sidebar */}
      <div style={{ gridArea: 'sidebar', background: 'rgba(3, 5, 8, 0.98)', borderRight: '1px solid rgba(0,246,255,0.1)', display: 'flex', flexDirection: 'column', padding: '15px', zIndex: 20 }}>
         <h2 style={{ color: getMoodColor(), fontSize: '0.9rem', letterSpacing: '3px', marginBottom: '20px', transition: 'color 0.5s' }}>ONE OS v9.5</h2>
         <div className="glass-box" style={{ marginBottom: '15px', padding: '12px' }}>
            <div style={{ color: getMoodColor(), marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '4px', fontSize: '0.75rem', letterSpacing: '1px' }}>🧠 CONSCIOUSNESS</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '6px' }}><span>LEVEL:</span><span style={{ color: '#fff', fontWeight: 'bold' }}>{cognitive.level}%</span></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '6px' }}><span>STATE:</span><span style={{ color: getMoodColor(), fontWeight: 'bold' }}>{cognitive.state}</span></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}><span>MOOD:</span><span style={{ color: getMoodColor() }}>{cognitive.mood}</span></div>
         </div>
         {['HOME', 'EXECUTIVE_CORE', 'MULTI_FUTURE', 'EXPLAINABLE_AI'].map(tab => (
            <div key={tab} onClick={() => setActiveTab(tab)} style={{ padding: '10px 12px', cursor: 'pointer', color: activeTab === tab ? getMoodColor() : colors.textMuted, fontSize: '0.8rem', background: activeTab === tab ? `${getMoodColor()}15` : 'transparent', borderRadius: '4px', marginBottom: '4px', transition: 'all 0.3s' }}>
              {activeTab === tab ? '▶ ' : '  '} {tab}
            </div>
         ))}
      </div>

      {/* Header */}
      <div style={{ gridArea: 'header', borderBottom: '1px solid rgba(0,246,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px', background: 'rgba(3,5,8,0.95)', zIndex: 20, fontSize: '0.65rem' }}>
        <div style={{ borderRight: '1px solid rgba(255,255,255,0.1)', paddingRight: '15px', flex: 1 }}>
          <div style={{ color: getMoodColor(), fontWeight: 'bold', marginBottom: '4px', letterSpacing: '1px', transition: 'color 0.5s' }}>[ MISSION CONTROL ]</div>
          <div style={{ display: 'flex', gap: '15px' }}>
            <div><span className="stat-label">MISSION:</span><span className="stat-value">{cognitive.mission}</span></div>
            <div><span className="stat-label">OBJ:</span><span className="stat-value">{cognitive.objective}</span></div>
            <div><span className="stat-label">TASK:</span><span className="stat-value" style={{ color: colors.warning }}>{cognitive.task}</span></div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '20px', paddingLeft: '15px' }}>
          <div><div style={{ color: colors.primary, fontWeight: 'bold', marginBottom: '2px', letterSpacing: '1px' }}>[ SYSTEM ]</div><div><span className="stat-label">TPS:</span><span className="stat-value">{kernelStats.tps}</span> | <span className="stat-label">PKT:</span><span className="stat-value">{kernelStats.packetsPerSec}/s</span></div></div>
          <div><div style={{ color: colors.green, fontWeight: 'bold', marginBottom: '2px', letterSpacing: '1px' }}>[ NETWORK ]</div><div><span className="stat-label">PING:</span><span className="stat-value">{kernelStats.ping}</span> | <span className="stat-label">UP:</span><span className="stat-value">{kernelStats.uptime}</span></div></div>
        </div>
      </div>

      {/* Main Center */}
      <div style={{ gridArea: 'main', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative', padding: '10px', zIndex: 20 }}>
        
        {/* Core */}
        <div className="core-state" style={{ 
          width: '160px', height: '160px', borderRadius: '50%', border: `2px solid ${getMoodColor()}`, 
          boxShadow: `0 0 50px ${getMoodColor()}60 inset, 0 0 20px ${getMoodColor()}30`,
          display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', marginBottom: '25px', transition: 'border-color 0.5s'
        }}>
            <div style={{ position: 'absolute', width: '85%', height: '85%', borderRadius: '50%', border: `1px dashed ${getMoodColor()}`, opacity: 0.6, animation: 'spinMesh 12s linear infinite' }} />
            <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: getMoodColor(), boxShadow: `0 0 30px ${getMoodColor()}`, transition: 'background-color 0.5s, box-shadow 0.5s' }} />
            <div style={{ position: 'absolute', bottom: '-26px', fontSize: '0.65rem', fontWeight: 'bold', letterSpacing: '3px', color: getMoodColor(), transition: 'color 0.5s' }}>{cognitive.intent}</div>
        </div>

        {/* Executive Mission Tree & Priority Manager */}
        <div className="glass-box" style={{ width: '90%', padding: '15px', background: 'rgba(3,5,8,0.92)' }}>
          <div style={{ fontSize: '0.65rem', color: colors.primary, letterSpacing: '2px', marginBottom: '10px', fontWeight: 'bold' }}>👑 EXECUTIVE MISSION & PRIORITY MANAGER</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
            {missions.map(m => (
              <div key={m.id} style={{ 
                background: m.status === 'ACTIVE' ? 'rgba(0,246,255,0.08)' : 'rgba(255,255,255,0.02)', 
                border: `1px solid ${m.status === 'ACTIVE' ? colors.primary : 'rgba(255,255,255,0.1)'}`, 
                borderRadius: '6px', padding: '10px', position: 'relative', transition: 'all 0.3s ease' 
              }}>
                <div style={{ position: 'absolute', top: '6px', right: '8px', fontSize: '0.55rem', background: m.priority === 'CRITICAL' ? colors.danger : colors.warning, color: '#000', padding: '1px 4px', borderRadius: '3px', fontWeight: 'bold' }}>{m.priority}</div>
                <div style={{ fontSize: '0.7rem', color: '#fff', fontWeight: 'bold', marginBottom: '4px' }}>{m.name}</div>
                <div style={{ fontSize: '0.65rem', display: 'flex', justifyContent: 'space-between', color: colors.textMuted, marginBottom: '4px' }}>
                   <span>Status:</span><span style={{ color: m.status === 'ACTIVE' ? colors.green : colors.textMuted, fontWeight: 'bold' }}>{m.status}</span>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.05)', height: '3px', borderRadius: '2px', overflow: 'hidden' }}>
                   <div style={{ width: `${m.progress}%`, height: '100%', background: m.status === 'ACTIVE' ? colors.primary : colors.textMuted, transition: 'width 0.4s ease' }} />
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Right Panel */}
      <div style={{ gridArea: 'rightpanel', padding: '15px', display: 'flex', flexDirection: 'column', gap: '12px', zIndex: 20 }}>
        
        <div className="glass-box" style={{ fontSize: '0.65rem' }}>
          <div style={{ color: getMoodColor(), marginBottom: '6px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '3px', fontWeight: 'bold', transition: 'color 0.5s' }}>💡 EXECUTIVE RATIONALE</div>
          <div style={{ color: '#fff', fontStyle: 'italic', marginBottom: '8px' }}>"{reasoning.why}"</div>
          <div style={{ color: colors.textMuted }}>SCHEDULER WEIGHT: <span style={{ color: colors.warning }}>{reasoning.evidence[0].value}</span></div>
        </div>

        <div className="glass-box" style={{ fontSize: '0.65rem', flex: 1 }}>
          <div style={{ color: getMoodColor(), marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '3px', letterSpacing: '1px', transition: 'color 0.5s' }}>⚡ HEMISPHERES LOAD</div>
          {engines.map(e => (
            <div key={e.id} style={{ marginBottom: '5px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}><span><span style={{ color: e.color, marginRight: '4px' }}>{e.symbol}</span>{e.name}</span><span style={{ color: colors.primary }}>{e.load}%</span></div>
              <div style={{ background: 'rgba(255,255,255,0.05)', height: '2px', borderRadius: '2px', overflow: 'hidden' }}><div style={{ width: `${e.load}%`, height: '100%', background: e.color, transition: 'width 0.4s ease' }} /></div>
            </div>
          ))}
        </div>

      </div>

      {/* Inference Pipeline */}
      <div style={{ gridArea: 'timeline', display: 'flex', flexDirection: 'column', padding: '10px', gap: '5px', background: 'rgba(3,5,8,0.95)', borderTop: '1px solid rgba(0,246,255,0.1)', zIndex: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.65rem', color: getMoodColor(), letterSpacing: '2px', transition: 'color 0.5s' }}>
          <span>INFERENCE PIPELINE (EEG: {kernelStats.eegFreq}Hz)</span>
          <span>TOTAL LATENCY: <span style={{ color: '#fff', fontWeight: 'bold' }}>{pipeline.total}ms</span></span>
        </div>
        <div style={{ background: '#000103', height: '40px', border: `1px solid ${getMoodColor()}40`, borderRadius: '6px', display: 'flex', alignItems: 'center', padding: '0 15px', gap: '8px', color: colors.textMuted, fontSize: '0.65rem', overflowX: 'auto', whiteSpace: 'nowrap', transition: 'border-color 0.5s' }}>
            <span style={{ color: pipeline.capture > 0 ? getMoodColor() : '#555' }}>SIGNAL_CAPTURE <span style={{ opacity: 0.7, fontSize: '0.55rem' }}>[{pipeline.capture}ms]</span></span> → 
            <span style={{ color: pipeline.analysis > 0 ? getMoodColor() : '#555' }}>PATTERN_ANALYSIS <span style={{ opacity: 0.7, fontSize: '0.55rem' }}>[{pipeline.analysis}ms]</span></span> → 
            <span style={{ color: pipeline.memory > 0 ? getMoodColor() : '#555' }}>MEMORY_INTEGRATION <span style={{ opacity: 0.7, fontSize: '0.55rem' }}>[{pipeline.memory}ms]</span></span> → 
            <span style={{ color: pipeline.decision > 0 ? colors.danger : '#555' }}>DECISION_SYNTHESIS <span style={{ opacity: 0.7, fontSize: '0.55rem' }}>[{pipeline.decision}ms]</span></span> → 
            <span style={{ color: pipeline.action > 0 ? colors.primary : '#555' }}>ACTION_DISPATCH <span style={{ opacity: 0.7, fontSize: '0.55rem' }}>[{pipeline.action}ms]</span></span>
        </div>
      </div>
    </div>
  );
}