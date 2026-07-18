import { useEffect, useRef } from "react";

export default function HeroAuroraBackground() {
  const containerRef = useRef(null);
  const animationRef = useRef(null);
  const mouseRef = useRef({ x: 0, y: 0, targetX: 0, targetY: 0 });
  const timeRef = useRef(0);
  const lastTimeRef = useRef(0);
  const themeRef = useRef('dark');

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Configuration
    const config = {
      reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches,
      isMobile: window.innerWidth < 768,
      waveCount: 4,
      darkColors: [
        { r: 59, g: 130, b: 246 },   // Electric Blue
        { r: 34, g: 211, b: 238 },  // Cyan
        { r: 139, g: 92, b: 246 },  // Purple
        { r: 99, g: 102, b: 241 },  // Indigo
      ],
      lightColors: [
        { r: 59, g: 130, b: 246 },   // Electric Blue
        { r: 34, g: 211, b: 238 },  // Cyan
        { r: 139, g: 92, b: 246 },  // Purple
        { r: 99, g: 102, b: 241 },  // Indigo
      ],
    };

    // Get current theme
    const updateTheme = () => {
      themeRef.current = document.body.classList.contains('light-mode') ? 'light' : 'dark';
      container.style.background = themeRef.current === 'dark' ? '#050816' : '#ffffff';
    };

    updateTheme();

    // Create wave elements
    const waves = [];
    for (let i = 0; i < config.waveCount; i++) {
      const wave = document.createElement("div");
      wave.className = "aurora-wave";
      wave.style.cssText = `
        position: absolute;
        border-radius: 50%;
        filter: blur(100px);
        opacity: 0.5;
        will-change: transform, opacity;
        pointer-events: none;
      `;
      container.appendChild(wave);
      waves.push({
        element: wave,
        baseX: Math.random() * 100,
        baseY: Math.random() * 100,
        speedX: (Math.random() - 0.5) * 0.04,
        speedY: (Math.random() - 0.5) * 0.02,
        scale: 0.8 + Math.random() * 0.4,
        phase: Math.random() * Math.PI * 2,
        colorIndex: i % config.darkColors.length,
      });
    }

    // Create noise overlay
    const noise = document.createElement("div");
    noise.className = "aurora-noise";
    noise.style.cssText = `
      position: absolute;
      inset: 0;
      opacity: 0.03;
      pointer-events: none;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    `;
    container.appendChild(noise);

    // Animation loop
    const animate = (timestamp) => {
      if (!lastTimeRef.current) lastTimeRef.current = timestamp;
      const deltaTime = timestamp - lastTimeRef.current;
      
      // Pause if tab is inactive
      if (deltaTime > 100) {
        lastTimeRef.current = timestamp;
        animationRef.current = requestAnimationFrame(animate);
        return;
      }

      lastTimeRef.current = timestamp;
      timeRef.current += deltaTime * 0.001;

      // Skip animation if reduced motion
      if (config.reducedMotion) {
        animationRef.current = requestAnimationFrame(animate);
        return;
      }

      // Smooth mouse following
      mouseRef.current.x += (mouseRef.current.targetX - mouseRef.current.x) * 0.05;
      mouseRef.current.y += (mouseRef.current.targetY - mouseRef.current.y) * 0.05;

      // Update waves
      waves.forEach((wave, i) => {
        const colors = themeRef.current === 'dark' ? config.darkColors : config.lightColors;
        const color = colors[wave.colorIndex];
        const t = timeRef.current + wave.phase;
        
        // Breathing effect
        const breathe = Math.sin(t * 0.8) * 0.15 + 1;
        const baseOpacity = themeRef.current === 'dark' ? 0.4 : 0.25;
        const opacity = baseOpacity + Math.sin(t * 0.5) * 0.15;
        
        // Drift movement
        const driftX = Math.sin(t * wave.speedX * 10) * 30;
        const driftY = Math.cos(t * wave.speedY * 10) * 20;
        
        // Parallax effect from mouse
        const parallaxX = mouseRef.current.x * (0.02 + i * 0.01);
        const parallaxY = mouseRef.current.y * (0.02 + i * 0.01);
        
        // Calculate position (percentage based)
        const x = wave.baseX + driftX + parallaxX;
        const y = wave.baseY + driftY + parallaxY;
        
        // Apply transforms
        const size = config.isMobile ? 300 : 500;
        const finalScale = wave.scale * breathe * (size / 500);
        
        wave.element.style.width = `${size * finalScale}px`;
        wave.element.style.height = `${size * finalScale}px`;
        wave.element.style.left = `${x}%`;
        wave.element.style.top = `${y}%`;
        wave.element.style.transform = `translate(-50%, -50%)`;
        wave.element.style.opacity = opacity;
        wave.element.style.background = `radial-gradient(circle, rgba(${color.r}, ${color.g}, ${color.b}, 0.6) 0%, rgba(${color.r}, ${color.g}, ${color.b}, 0) 70%)`;
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    // Mouse handlers
    const handleMouseMove = (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 100;
      const y = (e.clientY / window.innerHeight - 0.5) * 100;
      mouseRef.current.targetX = x;
      mouseRef.current.targetY = y;
    };

    const handleMouseLeave = () => {
      mouseRef.current.targetX = 0;
      mouseRef.current.targetY = 0;
    };

    // Visibility change handler
    const handleVisibilityChange = () => {
      if (document.hidden) {
        cancelAnimationFrame(animationRef.current);
      } else {
        lastTimeRef.current = 0;
        animationRef.current = requestAnimationFrame(animate);
      }
    };

    // Start animation
    animationRef.current = requestAnimationFrame(animate);

    // Event listeners
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseleave", handleMouseLeave);
    document.addEventListener("visibilitychange", handleVisibilityChange);

    // Cleanup
    return () => {
      cancelAnimationFrame(animationRef.current);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseleave", handleMouseLeave);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      waves.forEach(wave => wave.element.remove());
      noise.remove();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="aurora-background"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        zIndex: 0,
        pointerEvents: "none",
        background: "#050816",
        overflow: "hidden",
      }}
    />
  );
}
