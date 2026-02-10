const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

let drawing = false;

canvas.addEventListener("mousedown", () => (drawing = true));
canvas.addEventListener("mouseup", () => (drawing = false));
canvas.addEventListener("mouseleave", () => (drawing = false));
canvas.addEventListener("mousemove", draw);

function draw(e) {
  if (!drawing) return;
  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.arc(e.offsetX, e.offsetY, 14, 0, Math.PI * 2);
  ctx.fill();
}

function clearCanvas() {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  document.getElementById("result").innerText = "";
}

function send() {
  const small = document.createElement("canvas");
  small.width = 28;
  small.height = 28;
  const sctx = small.getContext("2d");

  const imgDataFull = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imgDataFull.data;

  let minX = canvas.width,
    minY = canvas.height;
  let maxX = 0,
    maxY = 0;

  for (let y = 0; y < canvas.height; y++) {
    for (let x = 0; x < canvas.width; x++) {
      let i = (y * canvas.width + x) * 4;
      let r = data[i];
      if (r > 10) {
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }
  }

  if (minX > maxX || minY > maxY) return;

  const w = maxX - minX;
  const h = maxY - minY;

  sctx.fillStyle = "black";
  sctx.fillRect(0, 0, 28, 28);

  sctx.drawImage(canvas, minX, minY, w, h, 4, 4, 20, 20);
  sctx.filter = "blur(1px)";

  const imgData = sctx.getImageData(0, 0, 28, 28).data;
  let input = [];

  for (let i = 0; i < imgData.length; i += 4) {
    let r = imgData[i];
    input.push(r / 255);
  }

  fetch("https://digit-ai-san.onrender.com/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: input }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("result").innerText = "Cyfra: " + data.digit;
    });
}
