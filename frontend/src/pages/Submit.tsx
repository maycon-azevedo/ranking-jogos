import { useEffect, useRef, useState } from "react";
import { useDashboard, useSubmitScores, useUpdateScore, useDeleteScore } from "../api/hooks";
import { Card } from "../components/Card";
import { Confetti } from "../components/Confetti";
import { GameDot } from "../components/GameDot";
import { Skeleton, SkeletonCard } from "../components/Skeleton";
import { useToast } from "../context/ToastContext";
import { ALL_GAMES, GAME_META, GameName } from "../types";
import styles from "./Submit.module.css";

export function SubmitPage() {
  const { data: dashboard, isLoading } = useDashboard();
  const submitMutation = useSubmitScores();
  const updateMutation = useUpdateScore();
  const deleteMutation = useDeleteScore();
  const { addToast } = useToast();

  const [attempts, setAttempts] = useState<Record<string, number>>({});
  const [skipped, setSkipped] = useState<Record<string, boolean>>({});
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState(1);
  const [showConfetti, setShowConfetti] = useState(false);
  const prevCompleted = useRef(0);

  const completedGames = dashboard?.triad.filter((t) => t.played).map((t) => t.game) ?? [];
  const pendingGames = ALL_GAMES.filter((g) => !completedGames.includes(g));

  useEffect(() => {
    if (completedGames.length === 3 && prevCompleted.current < 3 && prevCompleted.current > 0) {
      setShowConfetti(true);
    }
    prevCompleted.current = completedGames.length;
  }, [completedGames.length]);

  useEffect(() => {
    const init: Record<string, number> = {};
    for (const g of pendingGames) init[g] = 2;
    setAttempts(init);
  }, [dashboard?.triad.filter((t) => t.played).length]);

  if (isLoading) {
    return (
      <div style={{ maxWidth: 560 }}>
        <Skeleton width={200} height={24} radius={8} />
        <div style={{ marginTop: 8, marginBottom: 24 }}>
          <Skeleton width={160} height={14} radius={4} />
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <SkeletonCard height={140} />
          <SkeletonCard height={140} />
          <SkeletonCard height={140} />
        </div>
      </div>
    );
  }

  if (completedGames.length === 3) {
    return (
      <div style={{ maxWidth: 560 }}>
        <Confetti active={showConfetti} />
        <div className={styles.allDone}>
          <div className={styles.allDoneIcon}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
          <h2 className={styles.allDoneTitle}>Tudo registrado!</h2>
          <p className={styles.allDoneSub}>Você já completou a tríade de hoje.</p>
        </div>

        <h3 className={styles.editSectionTitle}>Seus resultados de hoje</h3>
        <div className={styles.gamesList}>
          {dashboard?.triad.filter((t) => t.played).map((t) => {
            const meta = GAME_META[t.game];
            const isEditing = editingId === t.score_id;

            return (
              <Card key={t.game} hover={false} style={{ borderLeft: `4px solid ${meta.color}` }}>
                <div className={styles.editRow}>
                  <div className={styles.gameName}>
                    <GameDot game={t.game} />
                    <span>{meta.name}</span>
                  </div>

                  {isEditing ? (
                    <div className={styles.editControls}>
                      <button
                        className={styles.editStepBtn}
                        onClick={() => setEditValue((v) => Math.max(1, v - 1))}
                        disabled={editValue <= 1}
                      >
                        −
                      </button>
                      <span className={styles.editStepValue} style={{ color: meta.color }}>{editValue}</span>
                      <button
                        className={styles.editStepBtn}
                        onClick={() => setEditValue((v) => v + 1)}
                      >
                        +
                      </button>
                      <button
                        className={styles.editSaveBtn}
                        onClick={async () => {
                          try {
                            await updateMutation.mutateAsync({ scoreId: t.score_id!, attempts: editValue });
                            setEditingId(null);
                            addToast("Resultado atualizado!");
                          } catch {
                            addToast("Erro ao atualizar", "error");
                          }
                        }}
                      >
                        Salvar
                      </button>
                      <button
                        className={styles.editCancelBtn}
                        onClick={() => setEditingId(null)}
                      >
                        ✕
                      </button>
                    </div>
                  ) : (
                    <div className={styles.editControls}>
                      <span className={styles.editAttempts} style={{ color: meta.color }}>
                        {t.attempts} {t.attempts === 1 ? "tent." : "tent."}
                      </span>
                      <button
                        className={styles.editBtn}
                        onClick={() => {
                          setEditingId(t.score_id);
                          setEditValue(t.attempts!);
                        }}
                        title="Editar"
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                          <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                        </svg>
                      </button>
                      <button
                        className={styles.deleteBtn}
                        onClick={async () => {
                          try {
                            await deleteMutation.mutateAsync(t.score_id!);
                            addToast("Resultado removido");
                          } catch {
                            addToast("Erro ao remover", "error");
                          }
                        }}
                        title="Remover"
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="3 6 5 6 21 6" />
                          <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                        </svg>
                      </button>
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    );
  }

  const hasGamesToSubmit = pendingGames.some((g) => !skipped[g] && attempts[g]);

  const handleSubmit = async () => {
    const scores = pendingGames
      .filter((g) => !skipped[g] && attempts[g])
      .map((g) => ({ game: g, attempts: attempts[g]! }));

    if (scores.length === 0) return;
    try {
      await submitMutation.mutateAsync(scores);
      addToast("Resultados salvos com sucesso!");
    } catch {
      addToast("Erro ao salvar resultados", "error");
    }
  };

  return (
    <div style={{ maxWidth: 560 }}>
      <h1 className={styles.title}>Registrar Resultados</h1>
      <p className={styles.date}>
        {new Date().toLocaleDateString("pt-BR", { day: "numeric", month: "long", year: "numeric" })}
      </p>

      <div className={styles.gamesList}>
        {pendingGames.map((game) => {
          const meta = GAME_META[game];
          const val = attempts[game] ?? 2;
          const isSkipped = !!skipped[game];

          return (
            <Card
              key={game}
              hover={false}
              style={{
                borderLeft: `4px solid ${meta.color}`,
                opacity: isSkipped ? 0.45 : 1,
                transition: "opacity 0.2s",
              }}
            >
              <div className={styles.gameHeader} style={{ marginBottom: isSkipped ? 0 : 16 }}>
                <div className={styles.gameName}>
                  <GameDot game={game} />
                  <span>{meta.name}</span>
                </div>
                <label className={styles.skipLabel}>
                  <input
                    type="checkbox"
                    checked={isSkipped}
                    onChange={(e) => setSkipped((p) => ({ ...p, [game]: e.target.checked }))}
                  />
                  Não joguei
                </label>
              </div>

              {!isSkipped && (
                <>
                  <div className={styles.stepper}>
                    <button
                      className={styles.stepperBtn}
                      onClick={() => setAttempts((p) => ({ ...p, [game]: Math.max(1, val - 1) }))}
                      disabled={val <= 1}
                    >
                      −
                    </button>
                    <div className={styles.stepperValue} style={{ color: meta.color }}>
                      {val}
                    </div>
                    <button
                      className={styles.stepperBtn}
                      onClick={() => setAttempts((p) => ({ ...p, [game]: val + 1 }))}
                    >
                      +
                    </button>
                  </div>
                  <p className={styles.stepperHint}>
                    {val === 1 ? "1 tentativa" : `${val} tentativas`}
                  </p>
                </>
              )}
            </Card>
          );
        })}
      </div>

      {completedGames.length > 0 && (
        <div className={styles.alreadyDone}>
          <h3 style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--text-muted)", marginBottom: 12 }}>
            Já Registrados
          </h3>
          <div className={styles.doneTags}>
            {completedGames.map((gid) => {
              const meta = GAME_META[gid as GameName];
              const score = dashboard?.triad.find((t) => t.game === gid);
              return (
                <span
                  key={gid}
                  className={styles.doneTag}
                  style={{ background: meta.color + "18", color: meta.color }}
                >
                  {meta.name}: {score?.attempts}
                </span>
              );
            })}
          </div>
        </div>
      )}

      <button
        className={styles.submitBtn}
        disabled={!hasGamesToSubmit || submitMutation.isPending}
        onClick={handleSubmit}
        style={{
          background: hasGamesToSubmit ? "var(--accent)" : "var(--bg-hover)",
          color: hasGamesToSubmit ? "#fff" : "var(--text-muted)",
        }}
      >
        {submitMutation.isPending ? "Salvando..." : "Salvar Resultados"}
      </button>
    </div>
  );
}
