package dev.ming.movies;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;

@Service
public class ReviewService {

    @Autowired
    private ReviewRepository reviewRepository;

    /**
     * MongoTemplate 是 Spring Data MongoDB 提供的一个类，用于简化与 MongoDB 数据库的交互。
     * 它封装了常见的数据库操作，使得开发者可以更方便地进行增删改查、聚合等操作，而无需直接编写大量的数据库访问代码。
     *
     * MongoTemplate 的主要功能
     * CRUD 操作：提供了创建、读取、更新和删除文档的基本功能。
     * 查询：支持各种复杂查询操作，包括条件查询、分页、排序等。
     * 聚合：支持聚合操作，例如分组、统计等。
     * 索引管理：支持创建和删除索引。
     * 事件监听：支持在操作前后添加事件监听器。
     */
    @Autowired
    private MongoTemplate mongoTemplate;

    public Review createReview(String reviewBody, String imdbId){
//        Review review = new Review(reviewBody);
//        reviewRepository.insert(review);
        //上面注释的两行合为下面的一行
        Review review = reviewRepository.insert(new Review(reviewBody));

        mongoTemplate.update(Movie.class)
                .matching(Criteria.where("imdbId").is(imdbId))
                .apply(new Update().push("reviewIds").value(review))
                .first();

        return review;
    }
}
