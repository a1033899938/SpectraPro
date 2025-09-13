// js/main.js
import { Carousel } from '../index/carousel.js';

// 3. 声明全局变量存储数据（后续渲染用）
// let siteData;


// 初始化轮播器
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // const response = await fetch('json/siteData.json'); // 异步请求JSON文件
        // siteData = await response.json();  // 解析JSON数据
        // renderSiteData(); // 渲染所有动态内容
        initCarousel();   // 初始化轮播（基于数据文件中的轮播数据）
    } catch (error){
        console.error('JSON数据加载失败，请检查路径或文件:', error);
    }
});

function initCarousel() {
    const myCarousel = new Carousel('.carousel');

    setTimeout(() => {
        console.log('开始自动播放');
        myCarousel.setAutoPlay(true);
    }, 20000);
}

// 每2秒打印一次header的宽度
setInterval(() => {
    const header = document.querySelector('header');
    if (header) {
        console.log('当前header宽度:', header.offsetWidth);
    } else {
        console.log('未找到header元素');
    }
}, 200);


// function renderSiteData() {
//     // 4.1 渲染网站基础信息（标题、Logo、GroupName）
//     document.getElementById('Site-title').textContent = siteData.siteInfo.title;
//     document.getElementById('logo-text').textContent = siteData.siteInfo.logoText;
//     document.getElementById('group-name').textContent = siteData.siteInfo.groupName;
//
//     // 4.2 渲染导航栏（动态生成li）
//     const navList = document.getElementById('nav-list');
//     siteData.navigation.forEach(navItem => {
//         const li = document.createElement('li');
//         li.innerHTML = `<a href="${navItem.link}"><strong>${navItem.name}</strong></a>`;
//         navList.appendChild(li);
//     });
//
//     // 4.3 渲染轮播图（动态生成slide）
//     const carouselContainer = document.getElementById('carousel-container');
//     siteData.carousel.forEach((slide, index) => {
//         const slideDiv = document.createElement('div');
//         // 第一张slide默认加active类
//         slideDiv.className = `carousel-slide ${index === 0 ? 'active' : ''}`;
//         slideDiv.innerHTML = `
//             <img src="${slide.imgSrc}" alt="${slide.altText}">
//             <div class="slide-caption">
//                 <h3>${slide.caption}</h3>
//             </div>
//         `;
//         carouselContainer.appendChild(slideDiv);
//     });
//
//     // 4.4 渲染分块1（News）
//     const newsSection = document.getElementById('news-section');
//     newsSection.querySelector('.news-title').textContent = siteData.otherSections.news.title;
//     newsSection.querySelector('.news-content').textContent = siteData.otherSections.news.content;
//     const newsLink = newsSection.querySelector('.news-link');
//     newsLink.textContent = siteData.otherSections.news.linkText;
//     newsLink.href = siteData.otherSections.news.link || '#'; // 若数据中没有link，默认#
//
//     // 4.5 渲染分块2（Papers）
//     document.getElementById('papers-section').textContent = siteData.otherSections.papers;
//
//     // 4.6 渲染标语区（Slogan）
//     const sloganSection = document.getElementById('slogan-section');
//     sloganSection.querySelector('.slogan-h1').textContent = siteData.otherSections.slogan.h1;
//     sloganSection.querySelector('.slogan-h2').textContent = siteData.otherSections.slogan.h2;
//     sloganSection.querySelector('.slogan-bold').textContent = siteData.otherSections.slogan.boldText;
//     sloganSection.querySelector('.slogan-italic').textContent = siteData.otherSections.slogan.italicText;
//     const sloganLink = sloganSection.querySelector('.slogan-link');
//     sloganLink.textContent = siteData.otherSections.slogan.linkText;
//     sloganLink.href = siteData.otherSections.slogan.linkHref;
//     // 渲染列表项
//     const sloganList = sloganSection.querySelector('.slogan-list');
//     siteData.otherSections.slogan.listItems.forEach(item => {
//         const li = document.createElement('li');
//         li.textContent = item;
//         sloganList.appendChild(li);
//     });
//     // 渲染引用
//     const sloganQuote = sloganSection.querySelector('.slogan-quote');
//     sloganQuote.textContent = siteData.otherSections.slogan.quoteText;
//     sloganQuote.cite = siteData.otherSections.slogan.quoteSource;
//
//     // 4.7 渲染商店区（Shop）
//     const shopSection = document.getElementById('shop-section');
//     const shopImg = shopSection.querySelector('.shop-img');
//     shopImg.src = siteData.otherSections.shop.imgSrc;
//     shopImg.alt = 'Shop Image'; // 可在数据中加altText，这里默认
//     shopSection.querySelector('.shop-info').textContent = siteData.otherSections.shop.infoText;
//
//     // 4.8 渲染成员区（Members）
//     const membersSection = document.getElementById('members-section');
//     siteData.members.forEach(member => {
//         // 动态生成成员卡片（对应原HTML的结构）
//         const memberDiv = document.createElement('div');
//         // 郑可心的卡片加zkx类（保持原样式）
//         if (member.name === '郑可心') memberDiv.className = 'zkx';
//         memberDiv.innerHTML = `
//             <img src="${member.imgSrc}" alt="${member.altText}">
//             <h3>${member.name}</h3>
//             <p>${member.desc}</p>
//         `;
//         membersSection.appendChild(memberDiv);
//     });
//
//     // 4.9 渲染订阅区（Newsletter）
//     const newsletterSection = document.getElementById('newsletter-section');
//     newsletterSection.querySelector('.newsletter-prompt').textContent = siteData.otherSections.newsletter.promptText;
//     const emailInput = newsletterSection.querySelector('input[type="email"]');
//     emailInput.placeholder = siteData.otherSections.newsletter.inputPlaceholder;
//     newsletterSection.querySelector('button[type="submit"]').textContent = siteData.otherSections.newsletter.buttonText;
//
//     // 4.10 渲染页脚（Contact & Address）
//     document.getElementById('footer-contact-title').textContent = siteData.contact.title;
//     const footerAddress = document.getElementById('footer-address');
//     // 渲染英文地址
//     const englishAddress = footerAddress.querySelector('.english-address');
//     siteData.contact.englishAddress.forEach(line => {
//         const p = document.createElement('p');
//         p.textContent = line;
//         englishAddress.appendChild(p);
//     });
//     // 渲染中文地址
//     const chineseAddress = footerAddress.querySelector('.chinese-address');
//     siteData.contact.chineseAddress.forEach(line => {
//         const p = document.createElement('p');
//         p.textContent = line;
//         chineseAddress.appendChild(p);
//     });
// }
