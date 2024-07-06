import logo from './logo.svg';
import './App.css';
// import api from './api/axiosconfig'; 
import api from './api/axiosconfig';
//导入axios的实例
//从 React 库中导入 useState 和 useEffect 这两个 React Hook，用于在函数组件中添加状态管理和生命周期处理的能力。
import {useState, useEffect} from 'react';
import Layout  from './compoments/Layout';
import {Routes,Route} from 'react-router-dom';
import Home from './compoments/home/Home';
import Header from './compoments/header/Header';
import Trailer from './compoments/trailer/Trailer';
import Reviews from './compoments/reviews/Reviews';
import NotFound from './compoments/notFound/NotFound';


function App() {
  
  const [movies, setMovies] = useState();
  const [movie, setMovie] = useState();
  const [reviews, setReviews] = useState();

  const getMovies = async () => {

    try{
      //定义一个异步函数 getMovies，用于从后端 API 获取电影数据。使用之前导入的 api 对象（Axios 实例）
      //发起 GET 请求获取 /api/v1/movies 路径的数据。成功时将数据设置到 movies 状态中，失败时打印错误信息。
      const response = await api.get("/api/v1/movies");
      console.log(response.data)
      console.log(movies)
      setMovies(response.data)
    }
    catch(err){
      console.log(err);
    }

  };

  //直接复制的这个const部分
  const getMovieData = async (movieId) => {
    try{
      const response = await api.get(`/api/v1/movies/${movieId}`);

      const singleMovie = response.data;

      setMovie(singleMovie);

      setMovies(singleMovie.reviews);

    }
    catch(error)
    {
      console.error(error);
    }
  }

  //使用 useEffect Hook，
  //在组件加载后调用 getMovies 函数来获取电影数据。传入空数组 [] 作为第二个参数，表示只在组件挂载时执行一次该效果函数。
  useEffect(() => {
    getMovies();
  },[])

  //渲染函数组件的 JSX 结构，返回一个 <div> 元素，其中 className='App' 表示应用了 App.css 中定义的样式。
  return (
    //路由Route: Layout--应用布局 Home--应用首页UI页面 Trailer--预告片链接组件
    <div className="App">
      <Header/>
      <Routes>
        <Route path="/" element={<Layout/>}>
          <Route path="/" element={<Home movies = {movies}/>}></Route>
          <Route path="/Trailer/:ytTrailerId" element={<Trailer/>}></Route>
          <Route path="/Reviews/:movieId" element={<Reviews getMovieData = {getMovieData}
          movie={movie} reviews={reviews} setReviews={setReviews}/>}></Route>
          <Route path="*" element={<NotFound/>}></Route>
        </Route>  
      </Routes>

    </div>
  );
}

//导出 App 组件，使其可以在其他地方被引用和使用。
export default App;

