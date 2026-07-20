import React, { useState, useEffect } from 'react';

export default function App() {
  const [activeTab, setActiveTab] = useState('EXPLAINABLE_AI');
  const [aiState, setAiState] = useState('SEARCHING');
  
  // Consciousness & Goal Tree
  const [cognitive, setCognitive] = useState({
    intent: 'SEARCHING', level: 72, state: 'Focused', mood: 'Curious',
    mission: 'EXPLORE_ENVIRONMENT', objective: 'Pattern Recognition', task: 'Scan incoming vectors',
    reflection: 'Scanning data streams. Baseline topology looks stable.'
  });

  // Phase 3: Explainable Cognition Context
  const [reasoning, setReasoning] = useState({
    why: "Awaiting sufficient data variance to trigger analysis.",
    evidence: [{ id: 'EV-01', label: 'Variance', value: '< 2%' }, { id: 'EV-02', label: 'Signal Noise', value: 'Normal' }],
    memory: [{ id: 'MEM-00', label: 'Idle State Ref', match: '99%' }]
  });

  const [kernelStats, setKernelStats] = useState({
    eegFreq: 24, eegWave: 'THETA', latency: 4.8, tps: 45.2, packetsPerSec: 304,
    sync: 99.4, ws: 'ONLINE', ping: '2ms', uptime: '05:01:22'
  });

  const [pipeline, setPipeline] = useState({ capture: 12, analysis: 0, memory: 0, decision: 0, action: 0, total: 12 });
  const [forecast, setForecast] = useState([
    { time: '+5s', event: 'Baseline continuity', prob: 98 },
    { time: '+15s', event: 'Minor latency fluctuation', prob: 45 }
  ]);

  const [engines, setEngines] = useState([
    { id: 'reasoning', name: 'REASONING', symbol: '◆', color: '#8E4DFF', load: 78, side: 'left' },
    { id: 'planning', name: 'PLANNING', symbol: '●', color: '#00F6FF', load: 64, side: 'left' },
    { id: 'learning', name: 'LEARNING', symbol: '✦', color: '#00FF88', load: 55, side: 'left' },
    { id: 'memory', name: 'MEMORY', symbol: '○', color: '#00FF88', load: 91, side: 'left' },
    { id: 'simulation', name: 'SIMULATION', symbol: '◇', color: '#00F6FF', load: 82, side: 'right' },
    { id: 'validator', name: 'VALIDATOR', symbol: '■', color: '#FFC84A', load: 88, side: 'right' },
    { id: 'reflection', name: 'REFLECTION', symbol: '◈', color: '#FFC84A', load: 75, side: 'right' },
    { id: 'execution', name: 'EXECUTION', symbol: '▶', color: '#00FF88', load: 40, side: 'right' },
  ]);

  const [packets, setPackets] = useState([]);
  const [dustLayers, setDustLayers] = useState({ bg: [], mid: [], fg: [] });
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Neural Dust Generation
  useEffect(() => {
    const createDust = (count, sizeMin, sizeMax, opacityMin, opacityMax) => 
      Array.from({ length: count }).map(() => ({
        x: Math.random() * 100, y: Math.random() * 100,
        size: Math.random() * (sizeMax - sizeMin) + sizeMin,
        opacity: Math.random() * (opacityMax - opacityMin) + opacityMin,
        speedMod: Math.random() * 1.5 + 0.5
      }));
    setDustLayers({
      bg: createDust(150, 0.5, 1, 0.05, 0.15),
      mid: createDust(100, 1, 2, 0.15, 0.3),
      fg: createDust(30, 2, 3.5, 0.4, 0.7)
    });
    const handleMouseMove = (e) => setMousePos({ x: (e.clientX / window.innerWidth - 0.5) * 30, y: (e.clientY / window.innerHeight - 0.5) * 30 });
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Cognitive Cycle Simulation (v9.0 - Added Reasoning Updates)
  useEffect(() => {
    let step = 0;
    const cycle = setInterval(() => {
      step = (step + 1) % 5;
      switch(step) {
        case 0:
          setAiState('SEARCHING');
          setCognitive({ intent: 'SEARCHING', level: 72, state: 'Focused', mood: 'Curious', mission: 'EXPLORE_ENVIRONMENT', objective: 'Pattern Recognition', task: 'Scan incoming vectors', reflection: 'Scanning data streams. Baseline topology looks stable.' });
          setReasoning({ why: "Awaiting sufficient data variance to trigger analysis.", evidence: [{ id: 'EV-01', label: 'Variance', value: '< 2%' }, { id: 'EV-02', label: 'Noise', value: 'Low' }], memory: [{ id: 'MEM-00', label: 'Idle State Ref', match: '99%' }] });
          setPipeline({ capture: 12, analysis: 0, memory: 0, decision: 0, action: 0, total: 12 });
          setKernelStats(prev => ({ ...prev, eegFreq: 24, eegWave: 'THETA' }));
          break;
        case 1:
          setAiState('LEARNING');
          setCognitive({ intent: 'LEARNING', level: 88, state: 'Hyper Focus', mood: 'Curious', mission: 'EXPLORE_ENVIRONMENT', objective: 'Feature Extraction', task: 'Integrate new syntax', reflection: 'I have seen a variation of this pattern before. Re-evaluating associative weights.' });
          setReasoning({ why: "Input signature matches historical anomaly cluster.", evidence: [{ id: 'EV-1A', label: 'Pattern Delta', value: '+14%' }, { id: 'EV-1B', label: 'Header Sync', value: 'Mismatch' }], memory: [{ id: 'MEM-41', label: 'Storm Event #18', match: '91%' }, { id: 'MEM-12', label: 'Data Corruption', match: '64%' }] });
          setPipeline({ capture: 14, analysis: 33, memory: 0, decision: 0, action: 0, total: 47 });
          setKernelStats(prev => ({ ...prev, eegFreq: 42, eegWave: 'GAMMA' }));
          break;
        case 2:
          setAiState('PREDICTING');
          setCognitive({ intent: 'PREDICTING', level: 96, state: 'Dreaming', mood: 'Creative', mission: 'FORECAST_TIMELINE', objective: 'Simulate Outcomes', task: 'Generate +1m horizon', reflection: 'Simulating branch futures. Scenario B yields 88% stability. Searching anomalies.' });
          setReasoning({ why: "Testing branching pathways to avoid execution bottleneck.", evidence: [{ id: 'EV-SIM', label: 'CPU Load Est.', value: '98%' }, { id: 'EV-NET', label: 'Bandwidth Drop', value: '-12%' }], memory: [{ id: 'MEM-88', label: 'Simulated Crash', match: '85%' }, { id: 'MEM-42', label: 'Optimal Reroute', match: '92%' }] });
          setPipeline({ capture: 14, analysis: 33, memory: 18, decision: 0, action: 0, total: 65 });
          setKernelStats(prev => ({ ...prev, eegFreq: 50, eegWave: 'GAMMA' }));
          setForecast([{ time: '+5s', event: 'Signal divergence detected', prob: 92 }, { time: '+15s', event: 'Execution layer overload', prob: 78 }]);
          break;
        case 3:
          setAiState('DECIDING');
          setCognitive({ intent: 'DECIDING', level: 98, state: 'Emergency', mood: 'Danger', mission: 'RESOLVE_CONFLICT', objective: 'Safety Override', task: 'Select optimal path', reflection: 'Alternative found. Probability of success meets threshold. Overriding loop.' });
          setReasoning({ why: "Scenario C provides highest survival probability with lowest latency.", evidence: [{ id: 'EV-VAL', label: 'Validation Score', value: '94.2' }, { id: 'EV-RISK', label: 'Failure Risk', value: '4%' }], memory: [{ id: 'MEM-77', label: 'Successful Override', match: '98%' }] });
          setPipeline({ capture: 14, analysis: 33, memory: 18, decision: 24, action: 0, total: 89 });
          setKernelStats(prev => ({ ...prev, eegFreq: 14, eegWave: 'ALPHA' }));
          break;
        case 4:
          setAiState('EXECUTING');
          setCognitive({ intent: 'EXECUTING', level: 84, state: 'Focused', mood: 'Focused', mission: 'ACTION_DISPATCH', objective: 'System Sync', task: 'Deploy payload', reflection: 'Decision locked. Dispatching execution packets to validation layer.' });
          setReasoning({ why: "Commit phase initiated based on validated decision matrix.", evidence: [{ id: 'EV-COM', label: 'Commit Hash', value: '0x8F2A' }], memory: [{ id: 'MEM-SYS', label: 'Standard Boot', match: '100%' }] });
          setPipeline({ capture: 14, analysis: 33, memory: 18, decision: 24, action: 7, total: 96 });
          setKernelStats(prev => ({ ...prev, eegFreq: 28, eegWave: 'BETA' }));
          break;
      }
    }, 5500); 
    return () => clearInterval(cycle);
  }, []);

  // Update Engines and Shoot Packets (Temporal Echoes)
  useEffect(() => {
    const interval = setInterval(() => {
      setKernelStats(prev => ({
        ...prev,
        tps: parseFloat((65 + (Math.random() - 0.5) * 4).toFixed(1)),
        latency: parseFloat((4.1 + (Math.random() - 0.5) * 0.4).toFixed(1)),
        packetsPerSec: 300 + Math.floor((Math.random() - 0.5) * 30)
      }));

      setEngines(prev => prev.map(e => {
        let loadMod = Math.floor(Math.random() * 10) - 5;
        if (cognitive.intent === 'LEARNING' && (e.id === 'learning' || e.id === 'memory')) loadMod = 25;
        if (cognitive.intent === 'PREDICTING' && (e.id === 'simulation' || e.id === 'planning')) loadMod = 30;
        if (cognitive.intent === 'DECIDING' && (e.id === 'reasoning' || e.id === 'validator')) loadMod = 35;
        return { ...e, load: Math.min(99, Math.max(20, e.load + loadMod)) };
      }));

      const randomEngine = engines[Math.floor(Math.random() * engines.length)];
      setPackets(prev => [...prev.slice(-25), {
        id: Date.now() + Math.random(), color: randomEngine.color, side: randomEngine.side, progress: 0,
        speed: 0.012 + (Math.random() * 0.005), history: [] 
      }]);
    }, 600);
    return () => clearInterval(interval);
  }, [cognitive.intent, engines]);

  useEffect(() => {
    const animInterval = setInterval(() => {
      setPackets(prev => prev.map(p => {
        const newHistory = [p.progress, ...p.history].slice(0, 4);
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

  const getDustAnimation = (layerSpeed) => {
    if (cognitive.intent === 'LEARNING') return `dustInward ${5 / layerSpeed}s infinite cubic-bezier(0.4, 0, 0.2, 1)`;
    if (cognitive.intent === 'EXECUTING') return `dustOutward ${3 / layerSpeed}s infinite ease-out`;
    if (cognitive.intent === 'PREDICTING') return `dustJitter ${2 / layerSpeed}s infinite linear`;
    return `dustFloat ${15 / layerSpeed}s infinite ease-in-out`;
  };

  const getPacketPos = (side, progress) => {
    const startX = side === 'left' ? 20 : window.innerWidth - 540;
    const endX = (window.innerWidth - 500) / 2;
    const centerY = window.innerHeight / 2 - 100;
    return { x: startX + (endX - startX) * progress, y: centerY + (progress - 0.5) * 80 };
  };

  return (
    <div style={{
      background: colors.bg, color: '#fff', minHeight: '100vh', fontFamily: "'Courier New', Courier, monospace",
      display: 'grid', gridTemplateColumns: '240px 1fr 260px', gridTemplateRows: '85px 1fr 100px',
      gridTemplateAreas: `"sidebar header header" "sidebar main rightpanel" "sidebar timeline timeline"`,
      overflow: 'hidden', position: 'relative'
    }}>
      <style>{`
        @keyframes coreSearch { 0%, 100% { transform: scale(1); filter: drop-shadow(0 0 15px ${getMoodColor()}); } 50% { transform: scale(1.02); filter: drop-shadow(0 0 25px ${getMoodColor()}); } }
        @keyframes coreLearn { 0%, 100% { transform: scale(0.95); filter: drop-shadow(0 0 40px ${getMoodColor()}); } 50% { transform: scale(1.08); filter: drop-shadow(0 0 10px ${getMoodColor()}); } }
        @keyframes corePredict { 0% { transform: translate(1px, 1px) scale(1.02); filter: drop-shadow(0 0 35px ${getMoodColor()}); } 25% { transform: translate(-1px, -1px) scale(0.98); } 50% { transform: translate(-1px, 1px) scale(1.03); filter: drop-shadow(0 0 50px ${getMoodColor()}); } 75% { transform: translate(1px, -1px) scale(0.99); } 100% { transform: translate(1px, 1px) scale(1.02); filter: drop-shadow(0 0 35px ${getMoodColor()}); } }
        @keyframes coreDecide { 0% { filter: drop-shadow(0 0 10px ${colors.danger}); transform: scale(1); } 50% { filter: drop-shadow(0 0 60px ${colors.danger}); transform: scale(1.1); } 100% { filter: drop-shadow(0 0 10px ${colors.danger}); transform: scale(1); } }
        @keyframes coreExecute { 0% { filter: drop-shadow(0 0 50px ${colors.primary}); transform: scale(1.1); } 100% { filter: drop-shadow(0 0 10px ${colors.primary}); transform: scale(1); } }
        @keyframes dustFloat { 0%, 100% { transform: translateY(0px) scale(1); } 50% { transform: translateY(-20px) scale(1.1); } }
        @keyframes dustInward { 0% { transform: scale(1.5) translate(0, 0); opacity: 0; } 50% { opacity: 1; } 100% { transform: scale(0.2) translate(0, 0); opacity: 0; } }
        @keyframes dustOutward { 0% { transform: scale(0.2); opacity: 1; } 100% { transform: scale(2); opacity: 0; } }
        @keyframes dustJitter { 0%, 100% { transform: translate(0,0); } 25% { transform: translate(2px, -2px); } 75% { transform: translate(-2px, 2px); } }
        @keyframes spinMesh { 100% { transform: rotate(360deg); } }
        @keyframes spinMeshReverse { 100% { transform: rotate(-360deg); } }
        @keyframes pulseHorizon { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; box-shadow: 0 0 15px ${getMoodColor()}; } }
        .core-SEARCHING { animation: coreSearch 4s infinite ease-in-out; }
        .core-LEARNING { animation: coreLearn 2s infinite ease-in-out; }
        .core-PREDICTING { animation: corePredict 1s infinite linear; }
        .core-DECIDING { animation: coreDecide 1s infinite cubic-bezier(0.2, 0.8, 0.2, 1); }
        .core-EXECUTING { animation: coreExecute 1s infinite ease-out; }
        .glass-box { background: ${colors.glass}; backdrop-filter: blur(16px); border: 1px solid ${getMoodColor()}40; border-radius: 8px; padding: 10px; transition: border-color 0.4s; }
        .stat-value { color: #fff; font-weight: bold; }
        .stat-label { color: ${colors.textMuted}; margin-right: 4px; }
      `}</style>

      {/* Neural Dust */}
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh', pointerEvents: 'none', zIndex: 1, overflow: 'hidden' }}>
        {['bg', 'mid', 'fg'].map((layer, idx) => dustLayers[layer].map((d, i) => (
            <div key={`${layer}-${i}`} style={{
              position: 'absolute', left: `${d.x}%`, top: `${d.y}%`, width: `${d.size}px`, height: `${d.size}px`, 
              background: layer === 'mid' ? getMoodColor() : '#fff', borderRadius: '50%', opacity: d.opacity,
              boxShadow: `0 0 ${d.size * 2}px ${layer === 'mid' ? getMoodColor() : '#fff'}`,
              transform: `translate(${mousePos.x * (idx+1)*0.5}px, ${mousePos.y * (idx+1)*0.5}px)`,
              animation: getDustAnimation(d.speedMod * (idx+1))
            }} />
        )))}
      </div>

      {/* Temporal Echo Packets */}
      <svg style={{ position: 'absolute', top: 85, left: 240, width: 'calc(100vw - 500px)', height: 'calc(100vh - 185px)', pointerEvents: 'none', zIndex: 10 }}>
        {packets.map(p => {
          const currentPos = getPacketPos(p.side, p.progress);
          return (
            <g key={p.id}>
              {p.history && p.history.map((histProg, idx) => {
                const histPos = getPacketPos(p.side, histProg);
                return <circle key={`${p.id}-hist-${idx}`} cx={histPos.x} cy={histPos.y} r={3 - (idx * 0.5)} fill={p.color} opacity={0.4 - (idx * 0.1)} style={{ filter: `blur(1px)` }} />;
              })}
              <circle cx={currentPos.x} cy={currentPos.y} r="4" fill={p.color} style={{ filter: `drop-shadow(0 0 10px ${p.color})` }} />
            </g>
          );
        })}
      </svg>

      {/* Sidebar: Consciousness Layer */}
      <div style={{ gridArea: 'sidebar', background: 'rgba(3, 5, 8, 0.98)', borderRight: '1px solid rgba(0,246,255,0.1)', display: 'flex', flexDirection: 'column', padding: '15px', zIndex: 20 }}>
         <h2 style={{ color: getMoodColor(), fontSize: '0.9rem', letterSpacing: '3px', marginBottom: '20px', transition: 'color 0.4s' }}>ONE OS v9.0</h2>
         <div className="glass-box" style={{ marginBottom: '15px', padding: '12px' }}>
            <div style={{ color: getMoodColor(), marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '4px', fontSize: '0.75rem', letterSpacing: '1px' }}>🧠 CONSCIOUSNESS</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '6px' }}><span>LEVEL:</span><span style={{ color: '#fff', fontWeight: 'bold' }}>{cognitive.level}%</span></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '6px' }}><span>STATE:</span><span style={{ color: getMoodColor(), fontWeight: 'bold' }}>{cognitive.state}</span></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}><span>MOOD:</span><span style={{ color: getMoodColor() }}>{cognitive.mood}</span></div>
         </div>
         {['HOME', 'WORLD SIM', 'EXPLAINABLE_AI', 'PREDICTION'].map(tab => (
            <div key={tab} onClick={() => setActiveTab(tab)} style={{ padding: '10px 12px', cursor: 'pointer', color: activeTab === tab ? getMoodColor() : colors.textMuted, fontSize: '0.8rem', background: activeTab === tab ? `${getMoodColor()}15` : 'transparent', borderRadius: '4px', marginBottom: '4px' }}>
              {activeTab === tab ? '▶ ' : '  '} {tab}
            </div>
         ))}
      </div>

      {/* Header: Goal Tree & Kernel */}
      <div style={{ gridArea: 'header', borderBottom: '1px solid rgba(0,246,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px', background: 'rgba(3,5,8,0.95)', zIndex: 20, fontSize: '0.65rem' }}>
        <div style={{ borderRight: '1px solid rgba(255,255,255,0.1)', paddingRight: '15px', flex: 1 }}>
          <div style={{ color: getMoodColor(), fontWeight: 'bold', marginBottom: '4px', letterSpacing: '1px' }}>[ MISSION CONTROL ]</div>
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
        
        {/* Phase 3: EXPLAINABLE COGNITION (Why & Reflection) */}
        <div className="glass-box" style={{ width: '85%', marginBottom: '20px', textAlign: 'center', background: 'rgba(3,5,8,0.8)', border: `1px solid ${getMoodColor()}80` }}>
          <div style={{ fontSize: '0.65rem', color: getMoodColor(), letterSpacing: '2px', marginBottom: '6px', fontWeight: 'bold' }}>EXPLAINABLE COGNITION: WHY THIS ACTION?</div>
          <div style={{ fontSize: '0.8rem', color: '#fff', fontStyle: 'italic', letterSpacing: '0.5px', marginBottom: '8px' }}>"{cognitive.reflection}"</div>
          <div style={{ fontSize: '0.7rem', color: colors.textMuted }}>REASONING: <span style={{ color: '#fff' }}>{reasoning.why}</span></div>
        </div>

        {/* Dynamic Core */}
        <div className={`core-${cognitive.intent}`} style={{ 
          width: '200px', height: '200px', borderRadius: '50%', border: `2px solid ${getMoodColor()}`, 
          boxShadow: `0 0 60px ${getMoodColor()}70 inset, 0 0 20px ${getMoodColor()}30`,
          display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative',
          transition: 'all 0.5s ease', marginBottom: '20px'
        }}>
            <div style={{ position: 'absolute', width: '85%', height: '85%', borderRadius: '50%', border: `1px dashed ${getMoodColor()}`, opacity: 0.6, animation: 'spinMesh 12s linear infinite' }} />
            <div style={{ position: 'absolute', width: '65%', height: '65%', borderRadius: '50%', border: `1px dotted ${getMoodColor()}`, opacity: 0.8, animation: 'spinMeshReverse 8s linear infinite' }} />
            <div style={{ width: '50px', height: '50px', borderRadius: '50%', backgroundColor: getMoodColor(), boxShadow: `0 0 40px ${getMoodColor()}, 0 0 80px ${getMoodColor()}`, transition: 'all 0.5s ease' }} />
            <div style={{ position: 'absolute', bottom: '-30px', fontSize: '0.65rem', fontWeight: 'bold', letterSpacing: '3px', color: getMoodColor(), textShadow: `0 0 8px ${getMoodColor()}` }}>{cognitive.intent}</div>
        </div>

        {/* Prediction Horizon */}
        <div className="glass-box" style={{ width: '75%', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 25px', background: 'rgba(3,5,8,0.9)', animation: aiState === 'PREDICTING' ? 'pulseHorizon 2s infinite' : 'none' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}><span style={{ fontSize: '0.6rem', color: colors.textMuted }}>CURRENT</span><span style={{ fontSize: '0.75rem', color: '#fff', fontWeight: 'bold' }}>NOW</span></div>
          <div style={{ flex: 1, height: '1px', background: `linear-gradient(90deg, ${colors.textMuted}40 0%, ${getMoodColor()}80 100%)`, margin: '0 15px', position: 'relative' }}>
             {aiState === 'PREDICTING' && <div style={{ position: 'absolute', top: '-2px', left: '0', width: '4px', height: '4px', background: getMoodColor(), borderRadius: '50%', boxShadow: `0 0 8px ${getMoodColor()}`, animation: 'dustOutward 1.5s infinite linear' }} />}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}><span style={{ fontSize: '0.6rem', color: colors.textMuted }}>SIM_NODE</span><span style={{ fontSize: '0.75rem', color: getMoodColor(), fontWeight: 'bold' }}>+5s</span></div>
          <div style={{ flex: 1, height: '1px', background: `linear-gradient(90deg, ${getMoodColor()}80 0%, ${getMoodColor()}40 100%)`, margin: '0 15px' }} />
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}><span style={{ fontSize: '0.6rem', color: colors.textMuted }}>HORIZON</span><span style={{ fontSize: '0.75rem', color: colors.primary, fontWeight: 'bold' }}>+1m</span></div>
        </div>
      </div>

      {/* Right Panel: Load, Evidence & Activated Memory */}
      <div style={{ gridArea: 'rightpanel', padding: '15px', display: 'flex', flexDirection: 'column', gap: '15px', zIndex: 20 }}>
        
        {/* Phase 3: Evidence & Activated Memory */}
        <div className="glass-box" style={{ fontSize: '0.65rem' }}>
          <div style={{ color: colors.green, marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '3px', letterSpacing: '1px' }}>📂 EVIDENCE & MEMORY ARCHIVE</div>
          
          <div style={{ marginBottom: '10px' }}>
            <span style={{ color: colors.textMuted }}>[ ACTIVE EVIDENCE ]</span>
            {reasoning.evidence.map(ev => (
              <div key={ev.id} style={{ display: 'flex', justifyContent: 'space-between', color: '#fff', marginTop: '3px' }}>
                <span>{ev.label}</span><span style={{ color: colors.warning }}>{ev.value}</span>
              </div>
            ))}
          </div>

          <div>
            <span style={{ color: colors.textMuted }}>[ ACTIVATED MEMORY ]</span>
            {reasoning.memory.map(mem => (
              <div key={mem.id} style={{ display: 'flex', justifyContent: 'space-between', color: '#fff', marginTop: '3px' }}>
                <span>{mem.label}</span><span style={{ color: colors.green }}>{mem.match} MATCH</span>
              </div>
            ))}
          </div>
        </div>

        {/* Engine Load */}
        <div className="glass-box" style={{ fontSize: '0.7rem', flex: 1 }}>
          <div style={{ color: getMoodColor(), marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '3px', letterSpacing: '1px' }}>⚡ HEMISPHERES LOAD</div>
          {engines.map(e => (
            <div key={e.id} style={{ marginBottom: '6px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}><span><span style={{ color: e.color, marginRight: '4px' }}>{e.symbol}</span>{e.name}</span><span style={{ color: colors.primary }}>{e.load}%</span></div>
              <div style={{ background: 'rgba(255,255,255,0.05)', height: '2px', borderRadius: '2px' }}><div style={{ width: `${e.load}%`, height: '100%', background: e.color, transition: 'width 0.4s' }} /></div>
            </div>
          ))}
        </div>

      </div>

      {/* Inference Pipeline */}
      <div style={{ gridArea: 'timeline', display: 'flex', flexDirection: 'column', padding: '10px', gap: '5px', background: 'rgba(3,5,8,0.95)', borderTop: '1px solid rgba(0,246,255,0.1)', zIndex: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.65rem', color: getMoodColor(), letterSpacing: '2px' }}>
          <span>INFERENCE PIPELINE (EEG: {kernelStats.eegFreq}Hz)</span>
          <span>TOTAL LATENCY: <span style={{ color: '#fff', fontWeight: 'bold' }}>{pipeline.total}ms</span></span>
        </div>
        <div style={{ background: '#000103', height: '40px', border: `1px solid ${getMoodColor()}40`, borderRadius: '6px', display: 'flex', alignItems: 'center', padding: '0 15px', gap: '8px', color: colors.textMuted, fontSize: '0.65rem', overflowX: 'auto', whiteSpace: 'nowrap' }}>
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