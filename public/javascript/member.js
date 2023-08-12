const member_name = document.querySelector("#name");
const msg_ctn = document.querySelector(".msg-ctn");
const msg_parent = document.createElement("div");
msg_parent.classList.add("msg_parent");
const loadMore = document.querySelector(".loadmore");
const comment_form = document.querySelector("#msg_form");
const comment_textarea = document.querySelector("#comment_form textarea");
let counter = 0;

//msg_item_maker輸入參數為DB回傳的資料
//Data type = array
//array裡面的每個元素都是object
function msg_item_maker(msgColleciton) {
  if (msgColleciton.length < 5) {
    loadMore.style.display = "none";
    // const msg_itme = document.createElement("div");
    // msg_itme.classList.add("msg-item");
    // let template = `<p>Be the first to comment</p>`;
    // msg_itme.innerHTML = template;
    // msg_parent.appendChild(msg_itme);
    // msg_ctn.appendChild(msg_parent);
  } else {
    for (let i = 0; i < msgColleciton.length; i++) {
      const msg_itme = document.createElement("div");
      msg_itme.classList.add("msg-item");
      let template = `
                <div class="msg-left">	
                    <img src="/pic/msg-person.png" alt="msg-person" />
                    <p>${msgColleciton[i].name}</p>	
                </div>	
                <div class="msg-mid">	
                    <p>	
                    ${msgColleciton[i].comment}	
                    </p>	
                </div>	
                <div class="msg-right">	
                    <div class="msg-btn">	
                        <button>edit</button>	
                        <button>del</button>	
                    </div>	
                    <p>${msgColleciton[i].date}</p>	
                </div>
            `;
      msg_itme.innerHTML = template;
      msg_parent.appendChild(msg_itme);
    }

    msg_ctn.appendChild(msg_parent);
  }
}

async function init() {
  const response = await fetch("/init");
  const data = await response.json();
  let { userInfo } = data;
  let { msg } = data;
  member_name.textContent = userInfo.name;
  console.log(`MSGcollection = ${msg}`);
  msg_item_maker(msg);
  return userInfo;
}

init();

loadMore.addEventListener("click", async () => {
  counter += 5;
  const response = await fetch(`/loadMore/${counter}`);
  const data = await response.json();
  msg_item_maker(data);
  console.log("執行loadmore");
});

comment_form.addEventListener("submit", (e) => {
  if (!comment_textarea.value) {
    e.preventDefault();
  }
});
