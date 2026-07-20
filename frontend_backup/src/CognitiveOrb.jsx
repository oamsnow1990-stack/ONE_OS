import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function CognitiveOrb({ state = 'LISTENING' }) {
  const mountRef = useRef(null);

  useEffect(() => {
    const currentMount = mountRef.current;
    if (!currentMount) return;

    // 1. Setup Scene, Camera, Renderer
    const width = currentMount.clientWidth;
    const height = currentMount.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 3.5;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    currentMount.appendChild(renderer.domElement);

    // 2. กำหนดสีตามสถานะของระบบ (Mood-reactive colors)
    const getStateColor = (s) => {
      switch (s) {
        case 'THINKING': return 0x9d4edd; // สีม่วง (กำลังประมวลผล)
        case 'ALERT': return 0xff4d4d;    // สีแดง (แจ้งเตือน/Error)
        case 'SPEAKING': return 0x00ff88; // สีเขียวมรกต (กำลังตอบสนอง)
        case 'LISTENING': 
        default: return 0x00f3ff;         // สีฟ้า Cyan (กำลังรอฟังคำสั่ง)
      }
    };

    const activeColor = getStateColor(state);

    // 3. สร้างโครงข่าย Orb ด้านนอก (Wireframe Icosahedron)
    const geometry = new THREE.IcosahedronGeometry(1.3, 3);
    const material = new THREE.MeshBasicMaterial({
      color: activeColor,
      wireframe: true,
      transparent: true,
      opacity: 0.75
    });
    const orb = new THREE.Mesh(geometry, material);
    scene.add(orb);

    // 4. สร้างแกนกลาง (Inner Glowing Core)
    const coreGeo = new THREE.SphereGeometry(0.5, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({ color: activeColor });
    const core = new THREE.Mesh(coreGeo, coreMat);
    scene.add(core);

    // 5. Animation Loop
    let animationFrameId;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // ความเร็วในการหมุนเปลี่ยนไปตามสถานะ (ถ้าคิดอยู่จะหมุนเร็วขึ้น)
      const rotationSpeed = state === 'THINKING' ? 0.04 : 0.012;
      orb.rotation.x += rotationSpeed;
      orb.rotation.y += rotationSpeed * 1.5;

      // เอฟเฟกต์กระพริบ/ขยายตัว (Pulse) เมื่ออยู่ในสถานะคิดหรือพูด
      if (state === 'THINKING' || state === 'SPEAKING') {
        const scale = 1 + Math.sin(elapsedTime * 8) * 0.12;
        core.scale.set(scale, scale, scale);
      } else {
        core.scale.set(1, 1, 1);
      }

      renderer.render(scene, camera);
    };

    animate();

    // 6. Handle Window Resize
    const handleResize = () => {
      if (!currentMount) return;
      const newWidth = currentMount.clientWidth;
      const newHeight = currentMount.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup เมื่อ Component ถูกทำลาย
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (currentMount) {
        currentMount.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
      coreGeo.dispose();
      coreMat.dispose();
      renderer.dispose();
    };
  }, [state]); // รันใหม่ทุกครั้งที่ State เปลี่ยน เพื่ออัปเดตสีและอนิเมชัน

  return (
    <div 
      ref={mountRef} 
      style={{ width: '100%', height: '100%', minHeight: '350px', position: 'relative' }} 
    />
  );
}
