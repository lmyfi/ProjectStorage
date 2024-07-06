# Java全栈应用：电影评论应用

## 项目概述

本项目是一个全栈应用，允许用户对电影进行评论。它使用MongoDB作为数据库，Java和Spring Boot构建后端，React用于前端开发。

## 核心特性

- **MongoDB**：用于存储电影数据和评论。
- **Spring Boot**：用于后端API的开发框架。
- **React**：用于构建用户界面的库。

## 后端设置

- 使用Spring Initializr初始化，配置Maven、Java和必要的依赖。
- 通过`application.properties`和`.env`文件配置MongoDB连接。
- 创建实体类（`Movies`和`Review`）以映射数据库文档。
- 在`MovieController`中实现MVC模式和RESTful端点。

## 前端设置

- 使用`create-react-app`进行项目脚手架搭建。
- 通过npm安装必要的组件，包括Axios、React-Bootstrap、FontAwesome、React-Player和React-Router-DOM。
- 使用CSS和Bootstrap进行样式设计，确保响应式布局。

## 使用方法

1. **后端**：启动Spring Boot应用程序以运行后端服务器。
2. **前端**：使用`npm start`启动React应用程序。

## 关键组件

- **电影评论**：用户可以查看电影并留下评论。
- **数据库连接**：使用环境变量安全连接到MongoDB。
- **API端点**：用于获取和操作电影数据的RESTful服务。
- **用户界面**：具有导航、电影展示和评论提交的响应式设计。

## 开发工具

- **IDE**：推荐使用IntelliJ IDEA进行后端开发。
- **前端编辑器**：推荐使用Visual Studio Code进行前端开发。