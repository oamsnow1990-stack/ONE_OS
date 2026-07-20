// ONE OS: คืนชีพ 3D Engine + ระบบเต้นตามเสียง
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 50;
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
container.appendChild(renderer.domElement);

// สร้างลูกแก้ว 3D (Neural Sphere)
const geometry = new THREE.SphereGeometry(15, 32, 16);
const material = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true });
const neuralSphere = new THREE.Mesh(geometry, material);
scene.add(neuralSphere);

// ระบบวิเคราะห์เสียง
let audioCtx, analyser;
function initAudio() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 64;
}

// ผูกปุ่ม START ให้เริ่มทำงานทั้งเสียงและกราฟิก
document.getElementById('start-btn').addEventListener('click', async () => {
    initAudio();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioCtx.createMediaStreamSource(stream).connect(analyser);
    
    document.getElementById('start-btn').style.display = 'none';
    const u = new SpeechSynthesisUtterance("ระบบ 3D และเสียงทำงานแล้วครับเจ้านาย");
    window.speechSynthesis.speak(u);
});

// ฟังก์ชัน Animation ลูปหลัก (ให้ลูกแก้วหมุนและเต้นตามเสียง)
function animate() {
    requestAnimationFrame(animate);
    
    // เต้นตามเสียง
    if (analyser) {
        let dataArray = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(dataArray);
        let volume = dataArray[2] / 128;
        neuralSphere.scale.set(1 + volume, 1 + volume, 1 + volume);
    }
    
    neuralSphere.rotation.x += 0.005;
    neuralSphere.rotation.y += 0.005;
    renderer.render(scene, camera);
}
animate();

// ดึงสถิติตัวเครื่อง (CPU/RAM)
async function fetchSystemMetrics() {
    try {
        const res = await fetch('http://127.0.0.1:8000/api/system/stats');
        const data = await res.json();
        document.getElementById('cpu-val').innerText = data.cpu_usage + '%';
        document.getElementById('ram-val').innerText = data.ram_usage + '%';
    } catch (e) {}
}
setInterval(fetchSystemMetrics, 2000);