* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #24152f;
  color: #fff8e7;
  font-family: Arial, Helvetica, sans-serif;
}

.app-shell {
  width: min(720px, 92vw);
}

.topbar {
  text-align: center;
  margin-bottom: 20px;
}

.topbar h1 {
  margin: 0;
  color: #ffb703;
  font-size: 2.7rem;
}

.topbar p {
  margin: 6px 0 0;
  color: #d7c6e8;
}

.game-panel {
  background: rgba(56, 35, 74, 0.9);
  border: 2px solid rgba(255, 183, 3, 0.4);
  border-radius: 18px;
  padding: 24px 20px 28px;
  text-align: center;
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.25);
}

.score {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  color: #fff8e7;
}

.rate {
  margin-top: 8px;
  color: #d7c6e8;
  font-size: 0.95rem;
}

.status {
  margin-top: 10px;
  color: #ffb703;
  font-weight: 700;
  min-height: 24px;
}

.click-button {
  margin-top: 18px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(180deg, #ffb703 0%, #f7a500 100%);
  color: #382000;
  font-size: 1.8rem;
  font-weight: 800;
  padding: 18px 32px;
  cursor: pointer;
  width: min(100%, 350px);
  transition: transform 0.1s ease, box-shadow 0.2s ease;
  box-shadow: 0 8px 18px rgba(255, 183, 3, 0.28);
}

.click-button:hover {
  transform: translateY(-1px);
}

.click-button:active {
  transform: scale(0.98);
}

.meter-wrap {
  margin-top: 28px;
}

.meter-title {
  color: #ffb703;
  font-weight: 700;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}

.meter-bar {
  height: 24px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.meter-fill {
  width: 0%;
  height: 100%;
  background: linear-gradient(90deg, #27d086 0%, #5ef0a9 100%);
  transition: width 0.15s linear;
}

.meter-label {
  margin-top: 8px;
  color: #d7c6e8;
  font-size: 0.9rem;
}

.rebirth-button {
  margin-top: 12px;
  background: #c44536;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  padding: 12px 24px;
  cursor: pointer;
}

.rebirth-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toolbar {
  margin-top: 22px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar button {
  background: rgba(255, 255, 255, 0.05);
  color: #fff8e7;
  border: 1px solid rgba(255, 183, 3, 0.6);
  border-radius: 8px;
  padding: 10px 18px;
  cursor: pointer;
  font-weight: 700;
}

.achievement {
  margin-top: 20px;
  color: #ffb703;
  font-style: italic;
  min-height: 24px;
}

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.62);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.hidden {
  display: none;
}

.modal-panel {
  width: min(620px, 92vw);
  background: #24152f;
  border: 2px solid rgba(255, 183, 3, 0.5);
  border-radius: 16px;
  padding: 18px 18px 22px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.modal-header h2 {
  margin: 0;
  color: #ffb703;
}

.close-button {
  border: none;
  background: transparent;
  color: #ffb703;
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
}

.upgrade-list {
  display: grid;
  gap: 8px;
}

.upgrade-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 183, 3, 0.3);
  border-radius: 10px;
  padding: 12px 14px;
}

.upgrade-copy {
  flex: 1;
  text-align: left;
}

.upgrade-name {
  display: block;
  font-weight: 700;
  color: #fff8e7;
}

.upgrade-meta {
  display: block;
  margin-top: 4px;
  color: #d7c6e8;
  font-size: 0.85rem;
}

.buy-button {
  border: none;
  border-radius: 8px;
  background: #ffb703;
  color: #382000;
  cursor: pointer;
  font-weight: 700;
  padding: 10px 12px;
  min-width: 120px;
}

@media (max-width: 540px) {
  .upgrade-item {
    flex-direction: column;
    align-items: stretch;
  }

  .buy-button {
    width: 100%;
  }
}
