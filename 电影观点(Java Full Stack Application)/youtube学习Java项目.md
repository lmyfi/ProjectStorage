# Java Full Stack

**时间：**2024-07-03 星期三

学习链接：https://www.youtube.com/watch?v=5PdEmeopJVQ

学习视频下的简介：
```markdown
In this full stack development course, you will learn how to create an application using MongoDb for the database, Java and Spring Boot for the backend, and React for the frontend.

You will learn to develop a movie review application that will feature a separation of concerns between the client code and the server code. By implementing this loosely coupled architecture, these two parts (implemented using different technologies) can evolve in parallel and independently from one another. 

✏️ Farhan Hasin Chowdhury teaches the backend section.
✏️ Gavin Lon teaches the frontend section. ‪@GavinLon‬ 

💻 Backend Code: https://github.com/fhsinchy/movieist
💻 Frontend Code: https://github.com/GavinLonDigital/mo...

🔗 Spring Initializr - https://start.spring.io/
🔗 JDK Download Page: https://www.oracle.com/java/technolog...
🔗 IntelliJ IDEA Download Page: https://www.jetbrains.com/idea/download/
🔗 Postman Download Page: https://www.postman.com/downloads/

🏗 MongoDB provided a grant to make this course possible.
```



## 后端（back-end）

### 数据库

​		数据库使用的是MongoDB，通过在线访问MongDB官网，创建一个DataBase，配置相关设置。主要有可以访问的IP Adress设置（0.0.0.0/0表示谁的可以访问这个MongDB数据库），然后使用了MongDB Compass的方式进行了与远程MongDB数据库进行连接的操作。



### Spring Boot初始化

​		**项目构建：** 使用Spring Initializr进行Spring Boot项目的构建，其中一些配置如下：使用Maven进行依赖管理、开发语言选择Java、Spring Boot版本我选择了3.3.1（与视频链接不同，可能是因为更新了，我图方便就选了这个）、项目相关的命名、JDK17、选择了一些依赖lomback、Spring Web以及Spring Data MongDB。

​		**项目初始化：**

-  使用IDEA打开Spring initializr生成的SpringBoot项目工程，打开后配置相关的JDK版本等，然后下载pom.xml中的依赖；

- 在application.properties中添加MongDB的数据库配置信息；
- 使用.env文件保存需要被保护的信息，如数据库的名称、用户名、密码还有集群名；在.gitignore文件末尾加上.env表示上传到github上时忽略这个文件；

- 使用.env文件内容：

  - 下载相关依赖,用于让.env文件起作用

    - ```xml
      <dependency>
      			<groupId>me.paulschwarz</groupId>
      			<artifactId>spring-dotenv</artifactId>
      			<version>2.5.4</version>
      		</dependency>
      ```

  - 将.env文件中的内容通过调用引用到application.properties中

    - 使用方式--：格式 ${env.变量名}

      - ```xml
        spring.data.mongodb.database=${env.MONGO_DATABASE}
        spring.data.mongodb.uri=mongodb+srv://${env.MONGO_USER}:${env.MONGO_PASSWORD}@${env.MONGO_CLUSTER}
        ```

  - 配置完成，就可以正常使用了



### spring boot项目中的MVC操作

​		**M:创建entity实体类:**在src.main.java.dev.ming.movies下新建Movies.java类，里面包含了的私有属性需要对应MongoDB数据库中，每一条数据所含有的字段信息。

- MongoDB的一条数据信息:

  - ```json
    {
      "_id": {
        "$oid": "6684e83d99b6fe9ed9476296"
      },
      "imdbId": "tt3915174",
      "title": "Puss in Boots: The Last Wish",
      "releaseDate": "2022-12-21",
      "trailerLink": "https://www.youtube.com/watch?v=tHb7WlgyaUc",
      "genres": [
        "Animation",
        "Action",
        "Adventure",
        "Comedy",
        "Family"
      ],
      "poster": "https://image.tmdb.org/t/p/w500/1NqwE6LP9IEdOZ57NCT51ftHtWT.jpg",
      "backdrops": [
        "https://image.tmdb.org/t/p/original/r9PkFnRUIthgBp2JZZzD380MWZy.jpg",
        "https://image.tmdb.org/t/p/original/faXT8V80JRhnArTAeYXz0Eutpv9.jpg",
        "https://image.tmdb.org/t/p/original/pdrlEaknhta2wvE2dcD8XDEbAI4.jpg",
        "https://image.tmdb.org/t/p/original/tGwO4xcBjhXC0p5qlkw37TrH6S6.jpg",
        "https://image.tmdb.org/t/p/original/cP8YNG3XUeBmO8Jk7Skzq3vwHy1.jpg",
        "https://image.tmdb.org/t/p/original/qLE8yuieTDN93WNJRmFSAEJChOg.jpg",
        "https://image.tmdb.org/t/p/original/vNuHqmOJRQXY0PBd887DklSDlBP.jpg",
        "https://image.tmdb.org/t/p/original/uUCc62M0I3lpZy0SiydbBmUIpNi.jpg",
        "https://image.tmdb.org/t/p/original/2wPJIFrBhzzAP8oHDOlShMkERH6.jpg",
        "https://image.tmdb.org/t/p/original/fnfirCEDIkxZnQEtEMMSgllm0KZ.jpg"
      ],
      "reviewIds": []
    }
    ```

- 对应数据编写实体类Movies.java

  - ```java
    @Document(collection = "movies")
    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public class Movies {
        @Id
        private ObjectId id;
        private String imdbId;
        private String title;
        private String trailerLink;
        private List<String> genres;
        private String poster;
        private List<String> backDrops;
        @DocumentReference
        private List<Review> reviewIds;
    }
    ```

    - Review实体类对象

      - ```java
        @Document(collection = "reviews")
        @Data
        @AllArgsConstructor
        @NoArgsConstructor
        public class Review {
            @Id
            private ObjectId id;
            private String body;
        }
        
        ```

​		**创建MovieController类：** 可以在同一路径下进行创建，这个文件里面主要用于向外部提供接口，以及对外部传回来的请求进行转发。

- 该类的主要结构如下:

  - ```java
    @RestController
    @RequestMapping("/api/v1/movies")
    public class MovieController {
    
        @GetMapping
        public ResponseEntity<String> allMovies(){
            return new ResponseEntity<String>("all movies !!", HttpStatus.OK);
        }
    }
    ```

​	

​		**编写服务接口/服务实现--（查询）：**服务接口（interface）主要用来定义服务，服务实现（serviceImplement）提供服务的具体实现过程。

​	

​	1.实现查询所有电影：

- 在MovieController中提供查询全部电影信息的接口

- 服务接口MovieRepository类定义服务，继承MongoRepository<Movie,ObjectId>(),该类中有findall()方法的实现

- 实现MovieService服务接口，autowire自动加载接口资源，编写查询所有电影的方法，返回所有的电影查询结果。

- 最后在MovieController中添加MovieService服务，并调用其提供的方法查询所有电影结果，并将其返回给浏览器。

  - ```java
    @RestController
    @RequestMapping("/api/v1/movies")
    public class MovieController {
    
        @Autowired
        private MovieService movieService;
    
        @GetMapping
        public ResponseEntity<List<Movie>> getAllMovies(){
            return new ResponseEntity<List<Movie>>(movieService.allMovies(), HttpStatus.OK);
        }
    }
    ```

​	

​	2.实现通过Id查询单个电影信息

- 步骤同上，主要是需要在MovieController和MovieService中添加新的方法

  - MovieService中添加的部分：

    - ```java
      //通过Id查询电影信息
          public Optional<Movie> singleMovieById(ObjectId id){
              return movieRepository.findById(id);
          }
      ```

  - MovieController中添加的部分

    - ```java
      @GetMapping("/{id}")
          public ResponseEntity<Optional<Movie>> getSingleMovieById(@PathVariable ObjectId id){
              return new ResponseEntity<Optional<Movie>>(movieService.singleMovieById(id), HttpStatus.OK);
          }
      ```

​	





​		**更新MongoDB数据库数据中字段信息--（改）**：新建ReviewController、ReviewRepository、ReviewService类，实现更新数据库中的"reviewIds"字段信息，编写流程与上面的查询差不多，但是需要注意的是这里需要更新数据库的信息，所有需要进行数据推送更新。

- ReviewRepository继承MongoRepository<Review,ObjectId>

- ReviewService实现服务，添加注解@Autowired自动加载ReviewRepository资源和MongoTemplate（MongoTemplate 是 Spring Data MongoDB 提供的一个类，用于简化与 MongoDB 数据库的交互)

  - 编写新增Review服务，实例化Review对象，并将其通过reviewRepository.insert(review)方法进行数据新增，之后使用mongoTemplate进行对数据的更新操作

    - ```java
      @Service
      public class ReviewService {
      
          @Autowired
          private ReviewRepository reviewRepository;
      
          @Autowired
          private MongoTemplate mongoTemplate;
      
          public Review createReview(String reviewBody, String imdbId){
              Review review = new Review(reviewBody);
              reviewRepository.insert(review);
              
              mongoTemplate.update(Movie.class)
                      .matching(Criteria.where("imdbId").is(imdbId))
                      .apply(new Update().push("reviewIds").value(review))
                      .first();
              return review;
          }
      ```

      




## 前端（front-end）

**时间：**2024-07-04 星期四

 使用nodejs构建项目。

### 1. 使用指令"npx create-react-app movie-gold-v1"创建Rect解释与作用

1. **npx**:
   - `npx` 是 Node.js 附带的一个命令行工具，专门用于运行 npm(Node Package Manager) 包里的可执行文件。
   - 当你使用 `npx` 时，它会在你的本地环境中查找指定的包，并执行其命令。如果没有找到，它会自动从 npm 仓库下载并执行该包。
2. **create-react-app**:
   - `create-react-app` 是一个官方的 React 工具，用于快速搭建 React 应用程序的开发环境。
   - 这个工具会为你创建一个新的 React 应用，配置好所有必要的开发依赖、脚手架和构建配置。
3. **movie-gold-v1**:
   - `movie-gold-v1` 是你希望创建的 React 应用程序的名称。
   - 运行该命令后，`create-react-app` 会在当前目录下创建一个名为 `movie-gold-v1` 的文件夹，并在其中生成所有项目所需的文件和文件夹结构。

### 2.删除生成的React项目中不需要的内容和使用NPM工具下载所需要的组件

- 删除不需要的文件并初始化项目

  - 删除App.test.js、reportWebvitals.js、setupTest.js文件

    - > **`App.test.js`**:
      >
      > - 这是一个默认的测试文件，用于演示如何编写测试用例。如果你当前不打算编写或运行测试，可以删除它以减少项目文件数。
      >
      > **`reportWebVitals.js`**:
      >
      > - 这个文件用于记录和报告 Web Vitals（Web 性能指标），例如首次内容绘制时间（FCP）等。如果你不打算监控应用性能，可以删除它及其相关的代码。
      >
      > **`setupTests.js`**:
      >
      > - 这是一个用于初始化 Jest 测试环境的文件。如果你不打算编写单元测试，可以删除它。

  - 在package.json中删除下面的内容

    - ```json
        "eslintConfig": {
          "extends": [
            "react-app",
            "react-app/jest"
          ]
        },
      ```

  - 在index.js中删除下面的内容

    - ```json
      import reportWebVitals from './reportWebVitals'; //导入的内容和使用的部分删除
      
      
      // If you want to start measuring performance in your app, pass a function
      // to log results (for example: reportWebVitals(console.log))
      // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
      reportWebVitals();
      ```

  - 完成上面的步骤，就可以在终端使用指令”npm start"进行项目启动

  

- 使用npm工具下载所需组件

  - ```shell
    npm install axios
    npm i react-bootstrap
    npm i @fortawesome/react-fontawesome
    npm i react-player
    npm i @fortawesome/free-solid-svg-icons
    npm i react-router-dom
    npm install @mui/material @emotion/react @emotion/styled
    npm install react-material-ui-carousel
    ```

  - 上面各个组件的作用

    - > 以下是对每个 npm 包的详细介绍，包括它们的作用和主要用途：
      >
      > ### 1. `axios`
      >
      > ```shell
      > npm install axios
      > ```
      >
      > - **作用**: `axios` 是一个基于 Promise 的 HTTP 客户端，用于浏览器和 Node.js。它简化了发送 HTTP 请求的过程，使得处理 AJAX 请求更加便捷。
      >
      > - 主要用途
      >
      >   :
      >
      >   - 发送 GET、POST、PUT、DELETE 等 HTTP 请求。
      >   - 处理请求和响应数据。
      >   - 支持拦截请求和响应。
      >   - 支持取消请求和自动转换 JSON 数据。
      >   - 在客户端和服务器端都可以使用。
      >
      > ### 2. `react-bootstrap`
      >
      > ```sh
      > npm i react-bootstrap
      > ```
      >
      > - **作用**: `react-bootstrap` 是 Bootstrap 组件的 React 实现，它提供了一组基于 Bootstrap 的 UI 组件，专门用于 React 项目中。
      > - **主要用途**:
      >   - 使用 Bootstrap 样式和组件（如按钮、表单、导航栏、模态框等）来快速构建响应式 Web 界面。
      >   - 提供与原生 Bootstrap 组件类似的 API，但更适合在 React 中使用。
      >
      > ### 3. `@fortawesome/react-fontawesome`
      >
      > ```sh
      > npm i @fortawesome/react-fontawesome
      > ```
      >
      > - **作用**: `@fortawesome/react-fontawesome` 提供了 Font Awesome 图标库的 React 组件，使得在 React 项目中使用 Font Awesome 图标变得更加方便。
      > - **主要用途**:
      >   - 在 React 组件中轻松使用 Font Awesome 图标。
      >   - 提供了一组可定制的图标组件，可以通过属性设置图标的大小、颜色、旋转等。
      >
      > ### 4. `react-player`
      >
      > ```sh
      > npm i react-player
      > ```
      >
      > - **作用**: `react-player` 是一个 React 组件，用于在应用中嵌入和播放各种媒体播放器（如 YouTube、Vimeo、SoundCloud 等）的视频和音频。
      > - **主要用途**:
      >   - 嵌入多种媒体播放器，支持播放各种流媒体服务的视频和音频。
      >   - 提供丰富的配置选项，如自动播放、循环播放、控制栏定制等。
      >
      > ### 5. `@fortawesome/free-solid-svg-icons`
      >
      > ```sh
      > npm i @fortawesome/free-solid-svg-icons
      > ```
      >
      > - **作用**: `@fortawesome/free-solid-svg-icons` 包含了 Font Awesome 的免费 Solid 风格图标，可以与 `@fortawesome/react-fontawesome` 一起使用。
      > - **主要用途**:
      >   - 提供大量免费的 Solid 风格图标，供 React 项目使用。
      >   - 与 `@fortawesome/react-fontawesome` 配合，轻松集成到 React 组件中。
      >
      > ### 6. `react-router-dom`
      >
      > ```sh
      > npm i react-router-dom
      > ```
      >
      > - **作用**: `react-router-dom` 是 React Router 的 DOM 绑定，使得在 React 应用中实现客户端路由变得非常简单。
      > - **主要用途**:
      >   - 定义客户端路由，并在不同的 URL 路径之间导航。
      >   - 提供 `<BrowserRouter>`, `<Route>`, `<Link>` 等组件，用于管理路由和导航。
      >   - 支持嵌套路由、动态路由、重定向等高级路由功能。
      >
      > ### 7. `@mui/material`, `@emotion/react`, `@emotion/styled`
      >
      > ```sh
      > npm install @mui/material @emotion/react @emotion/styled
      > ```
      >
      > - **作用**: 
      >   - `@mui/material` 是 Material-UI 的核心库，提供了一组基于 Material Design 规范的 React 组件。
      >   - `@emotion/react` 和 `@emotion/styled` 是 Emotion 库的一部分，用于在 React 项目中实现 CSS-in-JS。
      > - **主要用途**:
      >   - `@emotion/react` 和 `@emotion/styled`:
      >     - 通过 CSS-in-JS 技术在 React 组件中编写样式。
      >     - 使用 `@emotion/styled` 创建带有样式的 React 组件。
      >     - 动态生成和应用样式，支持主题定制。
      >
      > 
      >
      > ### 总结
      >
      > 通过安装和使用这些 npm 包，可以大大简化和加速 React 项目的开发过程，提供丰富的功能和组件，提升开发效率和用户体验。每个包都有其独特的用途，帮助开发者实现特定的功能需求。

### 3. 各组件使用

#### Axios组件

- **作用**: `axios` 是一个基于 Promise 的 HTTP 客户端，用于浏览器和 Node.js。它简化了发送 HTTP 请求的过程，使得处理 AJAX 请求更加便捷。
- **主要用途**:
  - 发送 GET、POST、PUT、DELETE 等 HTTP 请求。
  - 处理请求和响应数据。
  - 支持拦截请求和响应。
  - 支持取消请求和自动转换 JSON 数据。
  - 在客户端和服务器端都可以使用。

**使用**：

- 在生成的React项目的src目录下新建api目录，并新建axiosConfig.js文件用于配置axios

  - 内容

    - ```js
      import axios from 'axios';
      
      export default axios.create({
          baseURL: ' https://b94b-120-238-216-77.ngrok-free.app', //这里是自己使用ngrok http 8080生成的url
          headers: {"ngrok-skip-browser-warning": "true"}
      });
      
      ```

    - 

  - `axiosconfig.js` 文件的作用是创建一个经过预配置的 Axios 实例，用于在项目中发送 HTTP 请求。通过这种方式，可以集中管理 Axios 的配置，而不是在每次发送请求时都重复设置相同的配置参数。这样做有以下几个好处：

    1. **简化代码**: 避免在每个请求中重复设置相同的配置，如 `baseURL` 和默认的 `headers`。
    2. **集中管理**: 当需要更改配置（如更改 `baseURL`）时，只需要修改一个地方。
    3. **可维护性强**: 配置集中管理使得代码更易读和维护。

- 在React项目的App.js中使用配置好的axios

  - ```json
    import api from './api/axiosconfig'; //导入axios的实例
    ```

  

#### 实现轮播图 

**react-material-ui-carousel和@mui/material组件使用**

**组件作用：**

- `react-material-ui-carousel` 是一个基于 Material-UI 的 React 轮播组件，用于在应用中创建轮播图和轮播内容。
- `@mui/material` 是 Material-UI 的核心库，提供了一组基于 Material Design 规范的 React 组件。

**主要用途**:

- react-material-ui-carousel

  - 创建响应式的轮播图和轮播内容。

  - 提供自定义轮播项、导航按钮、自动播放等功能。

  - 与 Material-UI 组件和样式无缝集成。

- @mui/material

  - 使用 Material Design 组件构建现代 Web 应用界面。
  - 提供丰富的 UI 组件，如按钮、卡片、对话框、表单、表格等。

**以下是Hero.js文件使用这两个组件做轮播图的代码**

```js
import './Hero.css'
import Carousel from 'react-material-ui-carousel'
import { Paper } from '@mui/material'

const Hero = ({movies}) => {
    return(
        //设计轮播图
        <div className="movie-carousel-container">
            <Carousel>
                {
                    Array.isArray(movies) && movies.map(movie => {
                        return(
                            <Paper key={movie.id}>
                            <div className='movie-card-container'>
                                <div className='movie-card'>
                                    <div className='movie-detail'>
                                        <div className='movie-poster'>
                                            <img src={movie.poster} alt=""/>
                                        </div>
                                        <div className='movie-title'>
                                            <h4>{movie.title}</h4>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Paper>
                        )
                    })
                }
            </Carousel>
        </div>
    )
}

export default Hero;
```

我再执行轮播图设计过程中出现了许多的问题，被控了很久，也加深了我对前端中**解构Props**的认识

> 在 React 中，组件可以通过参数 `props` 接收父组件传递过来的数据。这些数据可以是任何类型的，比如字符串、数字、对象、数组等。当你在函数式组件或类组件中使用 `props`，它实际上是一个对象，包含了所有传递给组件的属性和值。
>
> 1. **Props 的意义**
>
> - **Props** 是 React 中用来传递数据的一种机制，是从父组件向子组件传递数据的主要方式之一。
> - **Props** 可以包含任何类型的数据，包括函数、对象、数组等。
>
> 2. **解构 Props 的意义**
>
> 当你在函数式组件中使用解构语法 `const Hero = ({ movies }) => {}`，它的作用是从 `props` 对象中提取出特定的属性（这里是 `movies`），并将其作为变量直接使用，而不需要通过 `props.movies` 的方式访问。
>
> **总结**
>
> - **Props** 是父组件传递给子组件的数据。
> - **解构 Props** 是一种方便的语法，用于从 `props` 对象中提取和使用特定属性，使代码更简洁、易读。





#### 修改前端展示样式

**修改App.css、Index.css和Hero.css**

​	**感想：**这部分直接就是无脑抄了，但是还是除了很多问题，刚开始因为这部分主要是关于CSS，所以在跟着视频敲完代码后发现不能复现它的样式，于是开始钻牛角尖一直看是不是那个css代码没弄对，在这反反复复折磨了快两三个小时，最后还是通过调试，以及在代码中使用{consolo.log()}进行了错误定位，发现了是背景图片一直出不来，之后使用postman进行接口测试，发现返回回来的数据中背景图片（backdrops）这个字段是空的，这也就是在前端一直展示不出来的原因。之后通过排查和修改，发现是数据实体类Movie中的backdrops字段因为自己以为是两个词组成的而命名字段为“backDrops”导致查询结果不对，修改成“backdrops”后就没问题。所以有时候解决问题还是要通过调试，排错的方式进行解决，不能无脑的钻牛角尖。





#### 编写导航栏

**文件：Header.js**

**时间：**2024-07-05 星期五 下午三点

**组件使用：**

- 组件作用
  - `FontAwesomeIcon` 是 Font Awesome（@fortawesome/react-fontawesome） 库中的一个组件，用于在 React 应用中展示图标。
  - `faVideoSlash` 是 Font Awesome（@fortawesome/free-solid-svg-icons） 提供的一个图标（视频关闭图标）
  - `Button` 是 React-Bootstrap（react-bootstrap/Button） 库中的一个组件，用于在 React 应用中创建按钮。
  - `Container` 是 React-Bootstrap（react-bootstrap/Container） 库中的一个组件，用于创建一个响应式的布局容器。
  - `Nav` 是 React-Bootstrap（react-bootstrap/Nav） 库中的一个组件，用于创建导航链接。
  - `Navbar` 是 React-Bootstrap（react-bootstrap/Navbar） 库中的一个组件，用于创建导航栏。
  - `NavLink` 是 React Router （react-router-dom）库中的一个组件，用于创建导航链接，支持路由导航。



​	**感想：**编辑导航栏的部分使用了react-bootstrap相关的组件，由于自己对于前端知识的认识比较浅，只看得懂简单的html\css\JavaScript代码，不知道在使用bootstrap组件时，应该导入这些组件所需的一些相关配置，因此再跟着视频作者进行代码完善的过程中，这里我的导航栏出现了混乱无序的情况，在这个错误上我花费了将近一天半的时间，后来通过自己的代码与作者的代码进行对比以及重复粘贴运行的调试方式最后定位出问题出现在了没有导入组件的原因：

> `import 'bootstrap/dist/css/bootstrap.min.css';` 的作用是将 Bootstrap 的 CSS 文件引入到你的 React 应用中。Bootstrap 是一个流行的 CSS 框架，提供预先定义好的样式和响应式布局，帮助快速构建响应式和视觉上吸引人的网页。

​	这个import 'bootstrap/dist/css/bootstrap.min.css';语句出现在了index.js文件中。



#### 编写预告片查看按钮

trailer.css 、trailer.js

**使用组件：**

- `import { useParams } from "react-router-dom"`

  - > `语句用于从 React Router 库中导入 `useParams` 钩子。这个钩子在使用 React Router 创建的单页应用（SPA）中非常有用，特别是当你需要访问当前 URL 的参数时。
    >
    > **作用：**`useParams` 是一个自定义钩子，用于访问当前路由的参数。这些参数通常是在定义路由路径时使用动态参数创建的。例如，在定义路径时使用 `:id` 作为参数，那么当用户访问该路径时，可以通过 `useParams` 获取 `id` 的值。

- `import ReactPlayer from "react-player"`

  - >  语句用于从 `react-player` 库中导入 `ReactPlayer` 组件。这是一个用于在 React 应用中嵌入和播放视频和音频的组件。
    >
    > 
    >
    > **作用**:`ReactPlayer` 是一个 React 组件，可以方便地在你的应用中嵌入各种媒体播放器。它支持多个平台，包括 YouTube、Vimeo、SoundCloud、Facebook、Twitch、Wistia、DailyMotion 和 HTML5 视频等。

**实现步骤：**

1.创建trailer/Trailer.js文件，用于获取视频资源和设置播放设置

```js
//内容
import { userParams } from "react-router-dom";
import ReactPlayer from "react-player";
import './Trailer.css';

import React from 'react'

const Trailer = () => {
  return (
    <div className="react-player-container">
        {(key!=null)?<ReactPlayer controls="true" playing={true} url={'https://www.youtube.com/watch?v=${key}'} 
        width= '100%' height='100%' />:null}
    </div>
  )
}

export default Trailer
```

2.在React应用文件App.js中配置trailer(预告片)路由，使其能找到预告片相关渲染内容

```js
//路由Route: Layout--应用布局 Home--应用首页UI页面 Trailer--预告片链接组件
    <div className="App">
      <Header/>
      <Routes>
        <Route path="/" element={<Layout/>}>
          <Route path="/" element={<Home movies = {movies}/>}></Route>
          <Route path="/Trailer/:ytTrailerId" element={<Trailer/>}></Route>
        </Route>  
      </Routes>

```



3.在轮播图Hero.js中添加播放按钮图标

```js
//导入组件
import { faCirclePlay } from '@fortawesome/free-solid-svg-icons';
//在轮播图中添加
//将播放按钮与预告片链接在一起
//<Link>标签属性中to={'/Trauker/${movie.trailer.substring(movie.trailer.length - 11)}'}表示只提取出预告片视频连接的视频ID
//因为数据库中的视频连接格式如--> trailerLink ： "https://www.youtube.com/watch?v=lroAhsDr2vI"; 最后面的ID刚好11位
<div className='movie-buttons-container'>
    <Link to={'/Trauker/${movie.trailer.substring()}'}{'/Trauker/${movie.trailer.substring(movie.trailer.length - 11)}'}>
        <div className='play-button-icon-container'>
            <FontAwesomeIcon className='play-button-icon' 
            icon = {faCirclePlay}
            />
        </div>
	</Link>
</div>

```

4.为添加的播放按钮修改样式，在Hero.css中添加

```css
.movie-buttons-container{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 300px;
}
.play-button-icon-container{
    padding: 0px;
    margin: 0px;
    width: 150px;
}
.play-button-icon{
    padding: 0px;
    margin:0px;
    color:gold;
    font-size: 3rem;
    transition: 0.3s;
    cursor: pointer;
}
.play-button-container:hover{
    font-size: 4rem;
    color: white;
}
@media only screen and (max-width: 8000px) {
    .movie-detail{
        flex-direction: column;
        align-items: center;
        top: 20px;
    }
}

```



**感想：**注意在使用`${}`进行React插值时，要使用Esc下面的 ` 符号，不然不起作用。



#### 编写撰写评论页面表单

reviewForm、reviews、notFound

**使用组件：**`import {Form, Button} from 'react-bootstrap'`



**感想：**这部分比较赶没有好好跟着做，都是直接使用现成的代码复制进行来，复制内容包括了reviewform、notFound、reviews文件夹，以及自己手动修改了Hero.js(添加review组件)、App.js（添加review路由和getMovieData等），除此之外由于直接复制的文件夹过来，导入 的文件路径也根据报错进行了修改。

