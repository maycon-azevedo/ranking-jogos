import { GAME_META, type GameName } from "../types";

export function GameDot({
  game,
  size = 10,
}: {
  game: GameName;
  size?: number;
}) {
  return (
    <span
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        background: GAME_META[game].color,
        display: "inline-block",
        flexShrink: 0,
      }}
    />
  );
}
