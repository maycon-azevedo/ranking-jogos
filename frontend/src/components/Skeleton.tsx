import styles from "./Skeleton.module.css";

export function Skeleton({
  width = "100%",
  height = 16,
  radius = 6,
}: {
  width?: string | number;
  height?: number;
  radius?: number;
}) {
  return (
    <div
      className={styles.skeleton}
      style={{ width, height, borderRadius: radius }}
    />
  );
}

export function SkeletonCard({ height = 80 }: { height?: number }) {
  return (
    <div
      className={styles.skeleton}
      style={{ width: "100%", height, borderRadius: 12 }}
    />
  );
}

export function SkeletonRow() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0" }}>
      <div className={styles.skeleton} style={{ width: 28, height: 28, borderRadius: "50%" }} />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6 }}>
        <div className={styles.skeleton} style={{ width: "60%", height: 14, borderRadius: 4 }} />
        <div className={styles.skeleton} style={{ width: "40%", height: 10, borderRadius: 4 }} />
      </div>
    </div>
  );
}
