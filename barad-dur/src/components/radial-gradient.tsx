import { useEffect, useState } from "react";

export const CursorGradient = () => {
    const [position, setPosition] = useState({ x: 0, y: 0 });

    const [theme, setTheme] = useState("light");

    const [backgroundColor, setBackgroundColor] = useState("radial-gradient(600px at 557px 134px, hsla(0, 0, 0, 0.15), transparent 80%)");
    useEffect(() => {
        const primaryHsl = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim().split(' ');
        const [h, s, l] = primaryHsl.map(value => value.trim());
        setBackgroundColor((_) => `radial-gradient(600px at ${position.x}px ${position.y}px, hsla(${h}, ${s}, ${l}, 0.15), transparent 95%)`);
    }, [position.x, position.y, theme]);

    return <div className="pointer-events-none fixed inset-0 z-40 transition duration-300" style={{ background: backgroundColor }}></div>;

};