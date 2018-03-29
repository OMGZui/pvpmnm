CREATE TABLE `boss` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  # 岗位要求
  `job_name` varchar(50) NOT NULL DEFAULT '0' COMMENT '岗位名字',
  `job_href` varchar(255) NOT NULL DEFAULT '0' COMMENT '详情链接',
  `money_min` int(11) NOT NULL DEFAULT '0' COMMENT '薪资最小',
  `money_max` int(11) NOT NULL DEFAULT '0' COMMENT '薪资最大',
  `address` varchar(50) NOT NULL DEFAULT '0' COMMENT '公司地址',
  `age` varchar(50) NOT NULL DEFAULT '0' COMMENT '年限',
  `certificate` varchar(50) NOT NULL DEFAULT '0' COMMENT '学历',
  # 公司情况
  `company_name` varchar(50) NOT NULL DEFAULT '0' COMMENT '公司名字',
  `company_href` varchar(255) NOT NULL DEFAULT '0' COMMENT '公司链接',
  `trade` varchar(50) NOT NULL DEFAULT '0' COMMENT '行业',
  `company_round` varchar(50) NOT NULL DEFAULT '0' COMMENT '轮次',
  `scale` varchar(50) NOT NULL DEFAULT '0' COMMENT '规模',
  # 发布情况
  `publish_name` varchar(50) NOT NULL DEFAULT '0' COMMENT '发布人昵称',
  `publish_href` varchar(255) NOT NULL DEFAULT '0' COMMENT '发布人头像',
  `publish_position` varchar(50) NOT NULL DEFAULT '0' COMMENT '发布人职位',
  `publish_time` varchar(50) NOT NULL DEFAULT '0' COMMENT '发布时间',
  `created_at` bigint(13) DEFAULT '0' COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COMMENT='boss直聘';
