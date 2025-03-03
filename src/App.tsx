import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import "./App.css";

function App() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Set up scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    containerRef.current.appendChild(renderer.domElement);

    // Create arm segments (shoulder, elbow, hand)
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const shoulder = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 32, 32),
      material
    );
    const elbow = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 32, 32),
      material
    );
    const hand = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 32, 32),
      material
    );

    scene.add(shoulder, elbow, hand);

    // WebSocket connection to receive pose data
    const socket = new WebSocket("ws://localhost:10000");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      shoulder.position.set(data.shoulder.x, data.shoulder.y, data.shoulder.z);
      elbow.position.set(data.elbow.x, data.elbow.y, data.elbow.z);
      hand.position.set(data.hand.x, data.hand.y, data.hand.z);
    };

    // Camera position
    camera.position.z = 2;

    // Render loop
    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }
    animate();

    // Cleanup
    return () => {
      socket.close();
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div className="App">
      <div ref={containerRef} className="canvas-container" />
    </div>
  );
}

export default App;
