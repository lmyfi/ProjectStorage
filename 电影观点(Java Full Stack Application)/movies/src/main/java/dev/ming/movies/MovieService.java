package dev.ming.movies;

import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class MovieService {
    @Autowired
    private MovieRepository movieRepository;

    //查询MongoDB中所有电影信息
    public List<Movie> allMovies(){
        return movieRepository.findAll();
    }
//    //通过Id查询电影信息
//    public Optional<Movie> singleMovieById(ObjectId id){
//        return movieRepository.findById(id);
//    }

    public Optional<Movie> singleMovieByImdbId(String imdbId){
        return movieRepository.findMoviesByImdbId(imdbId);
    }
}
