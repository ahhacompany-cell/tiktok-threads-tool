const accessKeyEl = document.getElementById("accessKey");
const secretKeyEl = document.getElementById("secretKey");
const coupangUrlEl = document.getElementById("coupangUrl");
const coupasUrlEl = document.getElementById("coupasUrl");
const memoEl = document.getElementById("memo");
const statusEl = document.getElementById("status");
const keyStatusEl = document.getElementById("keyStatus");

accessKeyEl.value = localStorage.getItem("coupas_access_key") || "";
secretKeyEl.value = localStorage.getItem("coupas_secret_key") || "";
coupangUrlEl.value = localStorage.getItem("last_coupang_url") || "";
coupasUrlEl.value = localStorage.getItem("last_coupas_url") || "";
memoEl.value = localStorage.getItem("threads_memo") || "";

if (accessKeyEl.value && secretKeyEl.value) {
  keyStatusEl.textContent = "저장된 API 키를 불러왔습니다.";
}

document.getElementById("saveKeys").onclick = () => {
  localStorage.setItem("coupas_access_key", accessKeyEl.value.trim());
  localStorage.setItem("coupas_secret_key", secretKeyEl.value.trim());
  keyStatusEl.textContent = "API 키를 이 브라우저에 저장했습니다.";
};

document.getElementById("clearKeys").onclick = () => {
  localStorage.removeItem("coupas_access_key");
  localStorage.removeItem("coupas_secret_key");
  accessKeyEl.value = "";
  secretKeyEl.value = "";
  keyStatusEl.textContent = "API 키를 삭제했습니다.";
};

document.getElementById("saveMemo").onclick = () => {
  localStorage.setItem("threads_memo", memoEl.value);
  statusEl.textContent = "메모를 저장했습니다.";
};

document.getElementById("clearMemo").onclick = () => {
  localStorage.removeItem("threads_memo");
  memoEl.value = "";
  statusEl.textContent = "메모를 지웠습니다.";
};

document.getElementById("clearLinks").onclick = () => {
  localStorage.removeItem("last_coupang_url");
  localStorage.removeItem("last_coupas_url");
  coupangUrlEl.value = "";
  coupasUrlEl.value = "";
  statusEl.textContent = "링크를 지웠습니다.";
};

document.getElementById("copyBtn").onclick = async () => {
  const text = coupasUrlEl.value.trim();
  if (!text) {
    statusEl.textContent = "복사할 링크가 없습니다.";
    return;
  }
  await navigator.clipboard.writeText(text);
  statusEl.textContent = "쿠파스 링크를 복사했습니다.";
};

document.getElementById("generateBtn").onclick = async () => {
  const accessKey = accessKeyEl.value.trim();
  const secretKey = secretKeyEl.value.trim();
  const coupangUrl = coupangUrlEl.value.trim();

  if (!accessKey || !secretKey) {
    statusEl.textContent = "API 키를 입력하세요.";
    return;
  }
  if (!coupangUrl) {
    statusEl.textContent = "쿠팡 상품 링크를 입력하세요.";
    return;
  }

  localStorage.setItem("last_coupang_url", coupangUrl);
  statusEl.textContent = "쿠파스 링크 생성 중...";

  try {
    const res = await fetch("/api/deeplink", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ accessKey, secretKey, coupangUrl })
    });

    const data = await res.json();

    if (!data.ok) {
      statusEl.textContent = "생성 실패: " + JSON.stringify(data.error || data);
      return;
    }

    coupasUrlEl.value = data.coupasUrl;
    localStorage.setItem("last_coupas_url", data.coupasUrl);
    await navigator.clipboard.writeText(data.coupasUrl);
    statusEl.textContent = "쿠파스 링크 생성 완료. 자동 복사했습니다.";
  } catch (err) {
    statusEl.textContent = "오류: " + err;
  }
};
