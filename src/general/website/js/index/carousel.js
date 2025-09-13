// js/modules/carousel.js
// 声明当前文件路径，模块化组织代码
import { CAROUSEL_CONFIG } from '../general/config.js';
// 从配置文件导入轮播图的配置参数

export class Carousel {
    // 导出Carousel类，使其可以被其他模块导入使用

    constructor(containerSelector) {
        // 构造函数，接收轮播图容器的选择器作为参数

        this.carousel = document.querySelector(containerSelector);
        // 获取轮播图容器元素

        this.slides = this.carousel.querySelectorAll('.carousel-slide');
        // 获取所有轮播项（幻灯片）

        this.prevBtn = this.carousel.querySelector('.carousel-prev');
        // 获取"上一张"按钮

        this.nextBtn = this.carousel.querySelector('.carousel-next');
        // 获取"下一张"按钮

        this.indicatorsContainer = this.carousel.querySelector('.carousel-indicators');
        // 获取指示器容器

        this.currentIndex = 0;
        // 当前显示的幻灯片索引，初始化为0（第一张）

        this.interval = null;
        // 用于存储自动播放的定时器ID

        this.config = CAROUSEL_CONFIG;
        // 存储轮播图配置

        this.init();
        // 初始化轮播图
    }

    init() {
        // 初始化方法，设置轮播图的初始状态

        // 创建指示器
        if (this.config.enableIndicators) {
            // 如果配置中启用了指示器
            this.createIndicators();
            // 调用创建指示器的方法
        } else {
            this.indicatorsContainer.style.display = 'none';
            // 否则隐藏指示器容器
        }

        // 显示/隐藏导航按钮
        if (!this.config.enableNavigation) {
            // 如果配置中禁用了导航按钮
            this.prevBtn.style.display = 'none';
            this.nextBtn.style.display = 'none';
            // 隐藏上一张和下一张按钮
        }

        // 添加事件监听
        this.prevBtn.addEventListener('click', () => this.prevSlide());
        // 给上一张按钮添加点击事件，点击时调用prevSlide方法

        this.nextBtn.addEventListener('click', () => this.nextSlide());
        // 给下一张按钮添加点击事件，点击时调用nextSlide方法

        // 鼠标悬停暂停
        this.carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
        // 鼠标进入轮播图时，停止自动播放

        this.carousel.addEventListener('mouseleave', () => {
            if (this.config.enableAutoPlay) {
                this.startAutoPlay();
            }
        });
        // 鼠标离开轮播图时，如果启用了自动播放，则重新开始自动播放

        // 自动播放
        if (this.config.enableAutoPlay) {
            this.startAutoPlay();
            // 如果配置中启用了自动播放，开始自动播放
        }
    }

    createIndicators() {
        // 创建指示器的方法

        this.indicatorsContainer.innerHTML = '';
        // 清空指示器容器

        this.slides.forEach((_, index) => {
            // 遍历所有幻灯片，为每个幻灯片创建一个指示器

            const indicator = document.createElement('div');
            // 创建一个div元素作为指示器

            indicator.textContent = index + 1;
            // 核心：添加序号文字（index从0开始，所以序号是 index + 1）

            indicator.className = `indicator ${index === 0 ? 'active' : ''}`;
            // 设置指示器的类名，第一张幻灯片的指示器默认添加active类

            indicator.addEventListener('click', () => this.goToSlide(index));
            // 给指示器添加点击事件，点击时跳转到对应的幻灯片

            this.indicatorsContainer.appendChild(indicator);
            // 将指示器添加到指示器容器中
        });

        this.indicators = this.carousel.querySelectorAll('.indicator');
        // 获取所有指示器元素，存储在实例变量中
    }

    goToSlide(index) {
        // 跳转到指定索引的幻灯片的方法

        // 移除当前活动状态
        this.slides[this.currentIndex].classList.remove('active');
        // 移除当前显示的幻灯片的active类

        if (this.indicators) {
            this.indicators[this.currentIndex].classList.remove('active');
            // 移除当前指示器的active类
        }

        // 更新索引
        this.currentIndex = index;
        // 将当前索引更新为目标索引

        // 添加新的活动状态
        this.slides[this.currentIndex].classList.add('active');
        // 给目标幻灯片添加active类

        if (this.indicators) {
            this.indicators[this.currentIndex].classList.add('active');
            // 给目标指示器添加active类
        }
    }

    nextSlide() {
        // 切换到下一张幻灯片的方法

        const nextIndex = (this.currentIndex + 1) % this.slides.length;
        // 计算下一张幻灯片的索引，使用取模运算实现循环

        this.goToSlide(nextIndex);
        // 跳转到下一张幻灯片
    }

    prevSlide() {
        // 切换到上一张幻灯片的方法

        const prevIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        // 计算上一张幻灯片的索引，加slides.length是为了避免出现负数

        this.goToSlide(prevIndex);
        // 跳转到上一张幻灯片
    }

    startAutoPlay() {
        // 开始自动播放的方法

        this.stopAutoPlay();
        // 先停止已有的自动播放，避免多个定时器同时运行

        this.interval = setInterval(() => this.nextSlide(), this.config.autoPlayDelay);
        // 设置定时器，每隔autoPlayDelay毫秒调用一次nextSlide方法
    }

    stopAutoPlay() {
        // 停止自动播放的方法

        if (this.interval) {
            clearInterval(this.interval);
            // 清除定时器

            this.interval = null;
            // 将interval设置为null
        }
    }

    // 添加一个公共方法用于外部控制
    setAutoPlay(enabled) {
        // 用于外部控制自动播放状态的方法

        this.config.enableAutoPlay = enabled;
        // 更新配置中的自动播放状态

        if (enabled) {
            this.startAutoPlay();
            // 如果启用自动播放，则开始自动播放
        } else {
            this.stopAutoPlay();
            // 如果禁用自动播放，则停止自动播放
        }
    }
}