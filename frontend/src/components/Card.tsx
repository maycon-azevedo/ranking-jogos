import { useState, type CSSProperties, type ReactNode } from "react";

export function Card({
  children,
  style,
  onClick,
  hover = true,
}: {
  children: ReactNode;
  style?: CSSProperties;
  onClick?: () => void;
  hover?: boolean;
}) {
  const [hov, setHov] = useState(false);

  return (
    <div
      onMouseEnter={() => hover && setHov(true)}
      onMouseLeave={() => setHov(false)}
      onClick={onClick}
      style={{
        background: "var(--bg-card)",
        borderRadius: 12,
        padding: 20,
        border: "1px solid var(--border)",
        transition: "transform 0.2s, box-shadow 0.2s",
        transform: hov ? "translateY(-2px)" : "none",
        boxShadow: hov
          ? "0 8px 24px var(--shadow)"
          : "0 1px 4px var(--shadow)",
        cursor: onClick ? "pointer" : "default",
        ...style,
      }}
    >
      {children}
    </div>
  );
}
