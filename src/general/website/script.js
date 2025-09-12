// alert("Hi~大家好")
let closet = 26;/*变量*/
const pant = 5.1415926 /*常量*/

let name = "HuShu"
let type = "Group"
console.log(name+type+"欢迎大家")

let para = `小明今天花了${closet+pant}元, 其中衣服${closet}元, 裤子${pant}元`
console.log(para)
console.log(para.length)
console.log(para.replace("今天", "昨天"))
console.log(para.slice(0, 17))
console.log(pant.toFixed(2))

console.log(pant < 5)
console.log(1 != 5)
console.log("60" == 60)
console.log("60" === 60)

if (pant < 5) {
    console.log("裤子好便宜")
} else if (5 <= pant < 10) {
    console.log("裤子有点贵")
}
else {
    console.log("润了")
}

// &&与, ||或
let array = [11, 22, 33, 44, 55, 66]
console.log(array)
console.log(array[0])
console.log(array.push(77))/*加入*/
console.log(array)
console.log(array.pop())/*删除最后一位*/
console.log(array.indexOf(66))/*索引*/
console.log(array.length)/*索引*/

for (let i = 0; i < array.length; i++) {
    console.log(array[i])
}

function sayHelloToSomeone(name) {
    console.log(`Hello, ${name}!!!`)
}

sayHelloToSomeone("HLS")

let group = document.querySelector("header h1")
console.log(group)
console.log(group.textContent)

group = document.querySelector(".menu")
console.log(group)

const zkx = document.querySelector(".zkx")
const type_line = document.querySelector(".type_line")
const button = document.querySelector(".button")

function creat_element() {
    if (type_line.value === "") {
        return;
    }
    const new_element = document.createElement("li");
    // new_element.textContent = type_line.value;/*只能插入纯文字,功能有限*/
    new_element.innerHTML = `
        <input class="cb" type="checkbox" class="打勾方块">
        <label>${type_line.value}</label>
        <button class="ljt">🚮</button>
    `
    zkx.append(new_element);
    type_line.value = "";

    const ljt = new_element.querySelector(".ljt");
    const cb = new_element.querySelector(".cb")

    ljt.addEventListener("click", function() {
        new_element.remove();
    })

    cb.addEventListener("change", function () {
        if (cb.checked) {
            new_element.remove()
            new_element.style.textDecoration = "line-through";
            new_element.style.color = "#999";
            zkx.append(new_element);
        } else {
            new_element.remove()
            new_element.style.textDecoration = "none";
            new_element.style.color = "";
            zkx.prepend(new_element);
        }
    })
}


type_line.addEventListener("keyup", function(e) {
    if (e.key == "Enter") {
        console.log(type_line.value)
    }
})/*监听操作*/


button.addEventListener("click", creat_element)




class Carousel {
    constructor() {
        this.carousel = document.querySelector('.carousel');
        this.slides = document.querySelectorAll('.carousel-slide');
        this.indicators = document.querySelectorAll('.indicator');
        this.prevBtn = document.querySelector('.carousel-prev');
        this.nextBtn = document.querySelector('.carousel-next');
        this.currentIndex = 0;
        this.interval = null;
        this.autoPlayDelay = 5000; // 5秒自动切换

        this.init();
    }

    init() {
        // 创建指示器
        this.createIndicators();

        // 添加事件监听
        this.prevBtn.addEventListener('click', () => this.prevSlide());
        this.nextBtn.addEventListener('click', () => this.nextSlide());

        // 指示器点击
        document.querySelectorAll('.indicator').forEach((indicator, index) => {
            indicator.addEventListener('click', () => this.goToSlide(index));
        });

        // 自动播放
        this.startAutoPlay();

        // 鼠标悬停暂停
        this.carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
        this.carousel.addEventListener('mouseleave', () => this.startAutoPlay());
    }

    createIndicators() {
        const indicatorsContainer = document.querySelector('.carousel-indicators');
        indicatorsContainer.innerHTML = '';

        this.slides.forEach((_, index) => {
            const indicator = document.createElement('div');
            indicator.className = `indicator ${index === 0 ? 'active' : ''}`;
            indicator.addEventListener('click', () => this.goToSlide(index));
            indicatorsContainer.appendChild(indicator);
        });
    }

    goToSlide(index) {
        this.slides[this.currentIndex].classList.remove('active');
        document.querySelectorAll('.indicator')[this.currentIndex].classList.remove('active');

        this.currentIndex = index;

        this.slides[this.currentIndex].classList.add('active');
        document.querySelectorAll('.indicator')[this.currentIndex].classList.add('active');
    }

    nextSlide() {
        const nextIndex = (this.currentIndex + 1) % this.slides.length;
        this.goToSlide(nextIndex);
    }

    prevSlide() {
        const prevIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.goToSlide(prevIndex);
    }

    startAutoPlay() {
        this.stopAutoPlay();
        this.interval = setInterval(() => this.nextSlide(), this.autoPlayDelay);
    }

    stopAutoPlay() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}

// 初始化轮播器
document.addEventListener('DOMContentLoaded', () => {
    new Carousel();
});