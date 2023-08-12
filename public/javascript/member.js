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
function msg_item_maker(userInfo, msgColleciton) {
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
      if (userInfo.id == msgColleciton[i].id) {
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
                <button class="edit-btn" msg_id = ${msgColleciton[i].msg_id}>edit</button>	
                <button class="del-btn" msg_id = ${msgColleciton[i].msg_id}>del</button>	
            </div>	
            <p>${msgColleciton[i].date}</p>	
        </div>
    `;
        msg_itme.innerHTML = template;
        msg_parent.appendChild(msg_itme);
      } else {
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
            <p>${msgColleciton[i].date}</p>	
        </div>
    `;
        msg_itme.innerHTML = template;
        msg_parent.appendChild(msg_itme);
      }
    }
  }
  msg_ctn.appendChild(msg_parent);
}

function listen_btn() {
  const del_btn = document.querySelectorAll(".del-btn");
  const edit_btn = document.querySelectorAll(".edit-btn");

  del_btn.forEach((btn) => {
    btn.addEventListener("click", async () => {
      yes = confirm("確定刪除留言？");
      console.log((yes = `${yes}`));
      if (yes) {
        response = await fetch("/getUserInfo");
        userInfo = await response.json();
        console.log(`userID = ${userInfo.id}`);
        msg_id = btn.getAttribute("msg_id");
        data = {
          user_id: userInfo.id,
          msg_id: msg_id,
        };
        delMsg = await fetch("/deleteMessage", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        window.location = "/member";
      }
    });
  });
  edit_btn.forEach((btn) => {
    btn.addEventListener("click", async () => {
      response = await fetch("/getUserInfo");
      userInfo = await response.json();
      console.log("userInfo = ", userInfo);
      console.log("編輯被點選");
    });
  });
}

async function init() {
  const response = await fetch("/init");
  const data = await response.json();
  let { userInfo } = data;
  let { msg } = data;
  member_name.textContent = userInfo.name;
  msg_item_maker(userInfo, msg);
  listen_btn();
}

init();

loadMore.addEventListener("click", async () => {
  counter += 5;
  const response = await fetch(`/loadMore/${counter}`);
  const data = await response.json();
  msg_item_maker(data.userInfo, data.msg);
  listen_btn();
});

//監聽留言板是否為空，空的就不能提交
comment_form.addEventListener("submit", (e) => {
  if (!comment_textarea.value) {
    e.preventDefault();
  }
});
