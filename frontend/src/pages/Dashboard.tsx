import { useNavigate } from "react-router-dom";
import { useDashboard } from "../api/hooks";
import { Avatar } from "../components/Avatar";
import { Card } from "../components/Card";
import { GameDot } from "../components/GameDot";
import { Skeleton, SkeletonCard } from "../components/Skeleton";
import { useAuth } from "../context/AuthContext";
import { ALL_GAMES, GAME_META, type GameName } from "../types";
import styles from "./Dashboard.module.css";

function formatDate(d: Date) {
  const months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
  return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
}

function getGreeting(): string {
  const h = new Date().getHours();
  if (h >= 5 && h < 12) return "Bom dia";
  if (h >= 12 && h < 18) return "Boa tarde";
  return "Boa noite";
}

function DashboardSkeleton() {
  return (
    <div>
      <div className={styles.header}>
        <div>
          <Skeleton width={220} height={28} radius={8} />
          <div style={{ marginTop: 8 }}>
            <Skeleton width={120} height={14} radius={4} />
          </div>
        </div>
      </div>
      <div style={{ marginBottom: 12 }}>
        <Skeleton width={140} height={11} radius={4} />
      </div>
      <div className={styles.triadGrid}>
        <SkeletonCard height={72} />
        <SkeletonCard height={72} />
        <SkeletonCard height={72} />
      </div>
      <div style={{ marginBottom: 12, marginTop: 28 }}>
        <Skeleton width={140} height={11} radius={4} />
      </div>
      <div className={styles.highlightsGrid}>
        <SkeletonCard height={80} />
        <SkeletonCard height={80} />
        <SkeletonCard height={80} />
      </div>
      <div style={{ marginBottom: 12, marginTop: 28 }}>
        <Skeleton width={160} height={11} radius={4} />
      </div>
      <SkeletonCard height={120} />
    </div>
  );
}

export function DashboardPage() {
  const { user } = useAuth();
  const { data, isLoading } = useDashboard();
  const navigate = useNavigate();

  if (isLoading || !data || !user) {
    return <DashboardSkeleton />;
  }

  const completedCount = data.triad.filter((t) => t.played).length;

  return (
    <div>
      <div className={styles.header}>
        <div>
          <h1 className={styles.greeting}>{getGreeting()}, {user.username}!</h1>
          <p className={styles.date}>{formatDate(new Date())}</p>
        </div>
        {data.streak > 0 && (
          <div className={styles.streak}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="var(--accent)" stroke="none">
              <path d="M12 23c-4.97 0-8-3.03-8-7 0-2.5 1.5-5.5 3-7.5.83-1.1 1.5-2.17 2-3.5.5 2 2 3.5 3 4.5 1.5-2 2.5-4.5 2.5-7.5 2 2 4.5 5 5 8.5.5 3.5-.5 5.5-1.5 7-1.5 2.5-3.5 5.5-6 5.5z" />
            </svg>
            {data.streak} dias
          </div>
        )}
      </div>

      {completedCount < 3 && data.friends_activity.length > 0 && (
        <div className={styles.reminderBanner}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round">
            <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 01-3.46 0" />
          </svg>
          <span>
            {data.friends_activity.slice(0, 2).map((f) => f.username).join(" e ")}
            {data.friends_activity.length > 2 && ` e mais ${data.friends_activity.length - 2}`}
            {" "}já {data.friends_activity.length === 1 ? "jogou" : "jogaram"} hoje!
          </span>
        </div>
      )}

      <h3 className={styles.sectionTitle}>Sua Tríade Diária</h3>
      <div className={styles.triadGrid}>
        {data.triad.map((t) => {
          const meta = GAME_META[t.game];
          return (
            <Card
              key={t.game}
              onClick={!t.played ? () => navigate("/submit") : undefined}
              style={{ borderLeft: `4px solid ${meta.color}`, cursor: t.played ? "default" : "pointer" }}
            >
              <div className={styles.triadCard}>
                <div>
                  <p className={styles.triadName}>{meta.name}</p>
                  {t.played ? (
                    <p className={styles.triadStatus} style={{ color: meta.color }}>
                      {t.attempts} {t.attempts === 1 ? "tentativa" : "tentativas"}
                    </p>
                  ) : (
                    <p className={styles.triadStatus} style={{ color: "var(--text-muted)" }}>
                      Pendente
                    </p>
                  )}
                </div>
                <div
                  className={styles.triadIcon}
                  style={{
                    background: t.played ? meta.color : "var(--bg-hover)",
                    color: t.played ? "#fff" : "var(--text-muted)",
                  }}
                >
                  {t.played ? "✓" : "—"}
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {completedCount < 3 && (
        <button className={styles.ctaBtn} onClick={() => navigate("/submit")}>
          Registrar Resultados
        </button>
      )}

      {data.champions.length > 0 && (
        <>
          <h3 className={styles.sectionTitle}>Campeão do Dia</h3>
          {data.champions.map((c) => (
            <div key={c.user_id} className={styles.championBanner}>
              <Avatar username={c.username} avatarUrl={c.avatar_url} size={42} />
              <div className={styles.championInfo}>
                <p className={styles.championTitle}>Campeão Provisório</p>
                <p className={styles.championName}>{c.username}</p>
                <p className={styles.championStats}>
                  {c.victories} {c.victories === 1 ? "vitória" : "vitórias"} · {c.total_attempts} tentativas
                </p>
              </div>
              {c.is_provisional && (
                <span className={styles.provisionalBadge}>Provisório</span>
              )}
            </div>
          ))}
        </>
      )}

      <h3 className={styles.sectionTitle}>Destaques de Hoje</h3>
      <div className={styles.highlightsGrid}>
        {data.highlights.map((h) => {
          const meta = GAME_META[h.game];
          return (
            <Card key={h.game} hover={false} style={{ padding: 16 }}>
              <div className={styles.highlightLabel}>
                <GameDot game={h.game} size={8} />
                <span className={styles.highlightGame}>{meta.name}</span>
              </div>
              {h.username ? (
                <div className={styles.highlightPlayer}>
                  <Avatar username={h.username} avatarUrl={h.avatar_url} size={28} />
                  <div>
                    <p className={styles.highlightName}>{h.username}</p>
                    <p className={styles.highlightAttempts} style={{ color: meta.color }}>
                      {h.attempts === 1 ? "1 tentativa" : `${h.attempts} tentativas`}
                    </p>
                  </div>
                </div>
              ) : (
                <div className={styles.emptyState}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" strokeWidth="1.5" strokeLinecap="round">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="8" y1="12" x2="16" y2="12" />
                  </svg>
                  <p>Nenhum resultado</p>
                </div>
              )}
            </Card>
          );
        })}
      </div>

      <h3 className={styles.sectionTitle}>Atividade dos Amigos</h3>
      <Card hover={false}>
        {data.friends_activity.length > 0 ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {data.friends_activity.map((f) => (
              <div key={f.user_id} className={styles.friendRow}>
                <Avatar username={f.username} avatarUrl={f.avatar_url} size={32} />
                <div className={styles.friendInfo}>
                  <p className={styles.friendName}>{f.username}</p>
                  <p className={styles.friendGames}>{f.games_played}/3 jogos registrados</p>
                </div>
                <div className={styles.friendDots}>
                  {ALL_GAMES.map((g: GameName) => (
                    <div
                      key={g}
                      style={{
                        width: 8,
                        height: 8,
                        borderRadius: "50%",
                        background: f.games.includes(g) ? GAME_META[g].color : "var(--bg-hover)",
                        transition: "background 0.3s",
                      }}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={styles.emptyState}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 00-3-3.87" />
              <path d="M16 3.13a4 4 0 010 7.75" />
            </svg>
            <p>Nenhum amigo registrou resultados hoje.</p>
          </div>
        )}
      </Card>
    </div>
  );
}
