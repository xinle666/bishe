<template>
  <div class="home">
    <!-- 动态背景 -->
    <div class="background-overlay"></div>

    <!-- 轮播图 -->
    <el-carousel :interval="4000" type="card" height="450px">
      <el-carousel-item v-for="(item, index) in images" :key="index">
        <img :src="require(`../assets/img/${item}`)" alt="背景图" class="carousel-image" />
      </el-carousel-item>
    </el-carousel>

    <!-- 欢迎文字 -->
    <div class="welcome-text">
      <h1>欢迎进入文协系统</h1>
      <p>在这里，您将体验到一场文字与科技的美妙交织</p>
    </div>

    <!-- 浮动按钮 -->
    <button class="floating-button">
      <i class="el-icon-edit"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: "HomeP",
  data() {
    return {
      user: '',
      images: [
        '1.jpg',
        '2.jpg',
        '3.jpg',
        '4.jpg',
        '5.jpg',
      ],
    }
  },
  created() {
    this.user = JSON.parse(sessionStorage.getItem("User"));
  },
}
</script>

<style scoped>
.home {
  position: relative;
  height: 100vh;
  background-color: #f5f5f5;
  overflow: hidden;
  font-family: 'Georgia', serif;
}

/* 动态背景渐变 */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.3));
  z-index: 0;
  animation: backgroundAnimation 15s infinite alternate;
}

@keyframes backgroundAnimation {
  0% {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.3));
  }
  100% {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.3));
  }
}

/* 轮播图样式 */
.el-carousel__item {
  background-color: transparent;
  transition: all 0.3s ease-in-out;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  filter: brightness(70%);
  transition: transform 0.5s ease, filter 0.5s ease;
}

.carousel-image:hover {
  transform: scale(1.05);
  filter: brightness(100%);
}

/* 欢迎文字样式 */
.welcome-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #437dd7;
  text-align: center;
  z-index: 10;
  opacity: 0;
  animation: fadeInText 2s 1s forwards;
}

@keyframes fadeInText {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

.welcome-text h1 {
  font-size: 48px;
  font-weight: 700;
  letter-spacing: 3px;
}

.welcome-text p {
  font-size: 24px;
  margin-top: 20px;
}

/* 浮动按钮 */
.floating-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #1f77b4;
  color: #fff;
  font-size: 24px;
  border: none;
  padding: 12px 18px;
  border-radius: 50%;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  z-index: 1000;
  transition: transform 0.3s ease;
}

.floating-button:hover {
  transform: scale(1.1);
}

/* 轮播图动画效果 */
.el-carousel__item:nth-child(odd) {
  background-color: rgba(255, 255, 255, 0.8);
}

.el-carousel__item:nth-child(even) {
  background-color: rgba(200, 200, 200, 0.7);
}
</style>
