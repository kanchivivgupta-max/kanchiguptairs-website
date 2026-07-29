// ============================================
// script.js — Interactive and 3D Visual features
// ============================================

// 1. Theme management (Dark Mode by Default)
const themeToggle = document.getElementById("theme-toggle");

const updateThemeUI = (isLight) => {
  if (isLight) {
    document.documentElement.classList.remove("dark");
    document.documentElement.classList.add("light");
    themeToggle.textContent = "🌙";
  } else {
    document.documentElement.classList.add("dark");
    document.documentElement.classList.remove("light");
    themeToggle.textContent = "☀️";
  }
};

// Initialize theme from storage, fallback to dark
const savedTheme = localStorage.getItem("theme") || "dark";
updateThemeUI(savedTheme === "light");

themeToggle.addEventListener("click", () => {
  const isLight = document.documentElement.classList.toggle("light");
  updateThemeUI(isLight);
  localStorage.setItem("theme", isLight ? "light" : "dark");
});

// 2. Time-based greeting
const hour = new Date().getHours();
const greeting = document.getElementById("greeting");

if (greeting) {
  if (hour < 12) {
    greeting.textContent = "Good morning, I'm";
  } else if (hour < 18) {
    greeting.textContent = "Good afternoon, I'm";
  } else {
    greeting.textContent = "Good evening, I'm";
  }
}

// 3. Auto-updating copyright year in footer
const yearSpan = document.getElementById("year");
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear();
}

// ============================================================
// 4. Interactive 3D Node Network Background (The "Agent Grid")
// ============================================================
const canvas = document.getElementById("nodes-canvas");
if (canvas) {
  const ctx = canvas.getContext("2d");
  
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);
  
  let particles = [];
  const particleCount = Math.min(80, Math.floor((width * height) / 15000)); // Responsive density
  const connectionDistance = 120;
  
  // Mouse tracking
  let mouse = { x: null, y: null, targetX: null, targetY: null, active: false };
  
  // Track system theme colors dynamically
  const getThemeColors = () => {
    const isLight = document.documentElement.classList.contains("light");
    return {
      accent: isLight ? "rgba(124, 92, 255, 0.4)" : "rgba(176, 158, 255, 0.25)",
      accentSolid: isLight ? "rgba(124, 92, 255, 0.7)" : "rgba(176, 158, 255, 0.6)",
      line: isLight ? "rgba(124, 92, 255, 0.08)" : "rgba(176, 158, 255, 0.05)",
    };
  };
  
  let colors = getThemeColors();
  
  // Recalculate colors on theme toggle
  themeToggle.addEventListener("click", () => {
    setTimeout(() => {
      colors = getThemeColors();
    }, 50);
  });

  class Particle {
    constructor() {
      this.reset();
      // Start at random depths
      this.z = Math.random() * 400 + 100;
    }

    reset() {
      // 3D coordinates relative to center
      this.x = (Math.random() - 0.5) * width * 1.5;
      this.y = (Math.random() - 0.5) * height * 1.5;
      this.z = 500; // Far plane
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.vz = -0.5 - Math.random() * 0.5; // Moving towards screen
      this.radius = Math.random() * 1.5 + 1;
    }

    update() {
      // Normal drift
      this.x += this.vx;
      this.y += this.vy;
      this.z += this.vz;

      // Mouse influence in 3D projection space
      if (mouse.active && mouse.x !== null) {
        // Project mouse coordinates to 3D plane at particle's current depth
        const fov = 400;
        const centerX = width / 2;
        const centerY = height / 2;
        const projMouseX = ((mouse.x - centerX) * this.z) / fov;
        const projMouseY = ((mouse.y - centerY) * this.z) / fov;

        const dx = projMouseX - this.x;
        const dy = projMouseY - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 150) {
          // Soft pull/push toward cursor
          this.x += (dx / dist) * 0.2;
          this.y += (dy / dist) * 0.2;
        }
      }

      // Reset if out of bounds or too close to screen
      if (this.z <= 50 || Math.abs(this.x) > width * 1.2 || Math.abs(this.y) > height * 1.2) {
        this.reset();
      }
    }

    project() {
      // 3D to 2D projection
      const fov = 400; // Field of view
      const centerX = width / 2;
      const centerY = height / 2;

      const scale = fov / (fov + this.z);
      const projX = this.x * scale + centerX;
      const projY = this.y * scale + centerY;
      const size = this.radius * scale * 2;

      return { x: projX, y: projY, size: size, opacity: scale };
    }
  }

  // Populate particles
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  // Handle window resizing
  window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  // Track mouse coordinates with dampening
  window.addEventListener("mousemove", (e) => {
    mouse.active = true;
    mouse.targetX = e.clientX;
    mouse.targetY = e.clientY;
  });

  window.addEventListener("mouseleave", () => {
    mouse.active = false;
    mouse.targetX = null;
    mouse.targetY = null;
  });

  // Animation Loop
  const animate = () => {
    ctx.clearRect(0, 0, width, height);

    // Smooth mouse position transitions
    if (mouse.targetX !== null) {
      if (mouse.x === null) {
        mouse.x = mouse.targetX;
        mouse.y = mouse.targetY;
      } else {
        mouse.x += (mouse.targetX - mouse.x) * 0.1;
        mouse.y += (mouse.targetY - mouse.y) * 0.1;
      }
    } else {
      mouse.x = null;
      mouse.y = null;
    }

    // Update and project particles
    const projectedParticles = [];
    particles.forEach((p) => {
      p.update();
      projectedParticles.push({
        particle: p,
        proj: p.project(),
      });
    });

    // Draw connecting lines (Representing Agent graph connections)
    for (let i = 0; i < projectedParticles.length; i++) {
      const p1 = projectedParticles[i];
      for (let j = i + 1; j < projectedParticles.length; j++) {
        const p2 = projectedParticles[j];
        
        // Calculate 3D distance for connectivity
        const dx = p1.particle.x - p2.particle.x;
        const dy = p1.particle.y - p2.particle.y;
        const dz = p1.particle.z - p2.particle.z;
        const dist3D = Math.sqrt(dx * dx + dy * dy + dz * dz);

        if (dist3D < connectionDistance) {
          // Opacity decreases as distance increases or particle gets further away
          const scaleOpacity = Math.min(p1.proj.opacity, p2.proj.opacity);
          const distOpacity = 1 - dist3D / connectionDistance;
          ctx.beginPath();
          ctx.strokeStyle = colors.line;
          ctx.globalAlpha = distOpacity * scaleOpacity * 0.8;
          ctx.lineWidth = 0.5 * scaleOpacity;
          ctx.moveTo(p1.proj.x, p1.proj.y);
          ctx.lineTo(p2.proj.x, p2.proj.y);
          ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 1.0; // Reset alpha

    // Draw particles
    projectedParticles.forEach((item) => {
      const { x, y, size, opacity } = item.proj;
      if (x >= 0 && x <= width && y >= 0 && y <= height) {
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        
        // Highlight cursor vicinity
        let color = colors.accent;
        if (mouse.x !== null) {
          const dx = x - mouse.x;
          const dy = y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 100) {
            color = colors.accentSolid;
          }
        }
        
        ctx.fillStyle = color;
        ctx.fill();
      }
    });

    requestAnimationFrame(animate);
  };

  animate();
}
