''' System Test Module

This test will simulate a run with the test data and produce checks to
ensure the results of processing the data are valid.

Any change to the test file data in the init setup  (td_dict) will affect
the tests in this module.  Be sure to adjust the results appropiately.

'''

from __future__ import division, print_function
import sys, os, datetime, time, re
import pytest
import unittest
import wp_migrate.cfg as cfg
import wp_migrate.util as util
import wp_migrate.flio as flio
import wp_migrate.wp_migrate as wp_migrate


def setup():
    '''(wpm.setup) setup for  testing'''
    print("SETUP!")
#    global wpm
#    wpm=wp_migrate.WPMigrate()




def teardown():
    '''(wpm.teardown) tear down for  testing'''
    print("TEAR DOWN!")


class TestWPM():
    trec1_a = """(157636, 'virtue_premium', 'a:3:{s:11:"font-family";s:50:"\'Lucida Sans Unicode\', \'Lucida Grande\', sans-serif";s:12:"font-options";}', 'yes');"""
    trec1_b = """(157636, 'virtue_premium', 'a:3:{s:11:"font-family";s:50:"\'Lucida Sans Unicode~#~#\'Lucida Grande~#~#sans-serif";s:12:"font-options";}', 'yes');"""

    rec1 = """(157636, 'virtue_premium', 'a:354:{s:8:"last_tab";s:1:"8";s:12:"boxed_layout";s:4:"wide";s:13:"footer_layout";s:5:"fourc";s:11:"logo_layout";s:8:"logoleft";s:21:"x1_virtue_logo_upload";a:5:{s:3:"url";s:58:"http://www.tpginc.net/blog/wp-content/uploads/TPG-Logo.png";s:2:"id";s:4:"1049";s:6:"height";s:3:"157";s:5:"width";s:3:"475";s:9:"thumbnail";s:66:"http://www.tpginc.net/blog/wp-content/uploads/TPG-Logo-150x150.png";}s:21:"x2_virtue_logo_upload";a:5:{s:3:"url";s:58:"http://www.tpginc.net/blog/wp-content/uploads/TPG-Logo.png";s:2:"id";s:4:"1049";s:6:"height";s:3:"157";s:5:"width";s:3:"475";s:9:"thumbnail";s:66:"http://www.tpginc.net/blog/wp-content/uploads/TPG-Logo-150x150.png";}s:15:"font_logo_style";a:9:{s:11:"font-family";s:50:"\'Lucida Sans Unicode\', \'Lucida Grande\', sans-serif";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:3:"400";s:10:"font-style";s:0:"";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"30px";s:11:"line-height";s:4:"40px";s:5:"color";s:7:"#bc0347";}s:15:"logo_below_text";s:0:"";s:18:"font_tagline_style";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:3:"400";s:10:"font-style";s:0:"";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"14px";s:11:"line-height";s:4:"20px";s:5:"color";s:7:"#444444";}s:16:"logo_padding_top";s:2:"25";s:19:"logo_padding_bottom";s:2:"10";s:17:"logo_padding_left";s:1:"0";s:18:"logo_padding_right";s:1:"0";s:15:"menu_margin_top";s:2:"40";s:18:"menu_margin_bottom";s:2:"10";s:20:"virtue_banner_upload";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:18:"virtue_banner_link";s:0:"";s:12:"header_style";s:6:"shrink";s:13:"header_height";s:3:"120";s:22:"side_header_menu_width";s:9:"33.333333";s:13:"sticky_header";s:1:"1";s:20:"shrink_center_header";s:1:"0";s:27:"shrink_center_header_height";s:3:"120";s:15:"m_sticky_header";s:1:"0";s:6:"topbar";s:1:"1";s:13:"topbar_mobile";s:1:"0";s:12:"topbar_icons";s:1:"0";s:16:"topbar_icon_menu";a:1:{i:0;a:12:{s:6:"icon_o";s:0:"";s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:14:"show_cartcount";s:1:"1";s:13:"topbar_search";s:1:"1";s:13:"topbar_widget";s:1:"0";s:13:"topbar_layout";s:1:"0";s:13:"choose_slider";s:4:"none";s:19:"above_header_slider";s:1:"0";s:25:"above_header_slider_arrow";s:1:"0";s:19:"home_cyclone_slider";s:0:"";s:11:"home_slider";a:2:{i:0;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}i:1;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:0:"";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:11:"slider_size";s:3:"400";s:17:"slider_size_width";s:4:"1140";s:15:"slider_autoplay";s:1:"1";s:16:"slider_pausetime";s:4:"7000";s:10:"trans_type";s:4:"fade";s:16:"slider_transtime";s:3:"600";s:15:"slider_captions";s:1:"0";s:11:"video_embed";s:0:"";s:13:"mobile_switch";s:1:"0";s:20:"choose_mobile_slider";s:4:"none";s:21:"mobile_cyclone_slider";s:0:"";s:18:"home_mobile_slider";a:2:{i:0;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}i:1;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:0:"";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:18:"mobile_slider_size";s:3:"300";s:24:"mobile_slider_size_width";s:3:"480";s:22:"mobile_slider_autoplay";s:1:"1";s:23:"mobile_slider_pausetime";s:4:"7000";s:17:"mobile_trans_type";s:4:"fade";s:23:"mobile_slider_transtime";s:3:"600";s:22:"mobile_slider_captions";s:1:"0";s:18:"mobile_video_embed";s:0:"";s:19:"home_sidebar_layout";s:4:"full";s:12:"home_sidebar";s:15:"sidebar-primary";s:15:"homepage_layout";a:2:{s:8:"disabled";a:11:{s:7:"placebo";s:7:"placebo";s:9:"block_two";s:10:"Image Menu";s:9:"block_one";s:10:"Page Title";s:11:"block_three";s:17:"Featured Products";s:10:"block_five";s:17:"Latest Blog Posts";s:9:"block_six";s:18:"Portfolio Carousel";s:11:"block_seven";s:9:"Icon Menu";s:11:"block_eight";s:14:"Portfolio Full";s:10:"block_nine";s:16:"On Sale Products";s:9:"block_ten";s:21:"Best Selling Products";s:12:"block_eleven";s:15:"Custom Carousel";}s:7:"enabled";a:3:{s:7:"placebo";s:7:"placebo";s:10:"block_four";s:12:"Page Content";s:12:"block_twelve";s:16:"Home Widget Area";}}s:15:"home_image_menu";a:2:{i:0;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}i:1;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:0:"";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:22:"home_image_menu_column";s:1:"3";s:15:"img_menu_height";s:3:"110";s:13:"product_title";s:0:"";s:24:"home_product_feat_column";s:1:"4";s:18:"home_product_count";s:1:"6";s:24:"home_product_feat_scroll";s:7:"oneitem";s:23:"home_product_feat_speed";s:1:"9";s:18:"product_sale_title";s:0:"";s:24:"home_product_sale_column";s:1:"4";s:23:"home_product_sale_count";s:1:"6";s:24:"home_product_sale_scroll";s:7:"oneitem";s:23:"home_product_sale_speed";s:1:"9";s:18:"product_best_title";s:0:"";s:24:"home_product_best_column";s:1:"4";s:23:"home_product_best_count";s:1:"6";s:24:"home_product_best_scroll";s:7:"oneitem";s:23:"home_product_best_speed";s:1:"9";s:10:"blog_title";s:0:"";s:15:"home_post_count";s:1:"2";s:16:"home_post_column";s:1:"2";s:14:"home_post_type";s:0:"";s:20:"home_post_word_count";s:2:"34";s:15:"portfolio_title";s:0:"";s:30:"home_portfolio_carousel_column";s:1:"3";s:30:"home_portfolio_carousel_height";s:0:"";s:29:"home_portfolio_carousel_count";s:1:"6";s:29:"home_portfolio_carousel_speed";s:1:"9";s:30:"home_portfolio_carousel_scroll";s:7:"oneitem";s:20:"home_portfolio_order";s:10:"menu_order";s:19:"portfolio_show_type";s:1:"0";s:22:"portfolio_show_excerpt";s:1:"0";s:21:"custom_carousel_title";s:0:"";s:26:"home_custom_carousel_items";a:2:{i:0;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}i:1;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:0:"";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:27:"home_custom_carousel_column";s:1:"4";s:27:"home_custom_carousel_scroll";s:7:"oneitem";s:17:"home_custom_speed";s:1:"9";s:9:"icon_menu";a:1:{i:0;a:12:{s:6:"icon_o";s:0:"";s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:21:"home_icon_menu_column";s:1:"3";s:13:"icon_bg_color";s:0:"";s:15:"icon_font_color";s:0:"";s:20:"portfolio_full_title";s:0:"";s:26:"portfolio_full_show_filter";s:1:"0";s:15:"home_port_count";s:1:"8";s:25:"home_portfolio_full_order";s:10:"menu_order";s:17:"home_port_columns";s:1:"4";s:26:"home_portfolio_full_height";s:0:"";s:22:"portfolio_full_masonry";s:1:"0";s:24:"portfolio_full_show_type";s:1:"0";s:27:"portfolio_full_show_excerpt";s:1:"0";s:23:"home_portfolio_lightbox";s:1:"0";s:17:"home_post_summery";s:7:"summery";s:14:"home_post_grid";s:1:"0";s:22:"home_post_grid_columns";s:10:"fourcolumn";s:19:"product_shop_layout";s:1:"4";s:11:"shop_layout";s:4:"full";s:12:"shop_sidebar";s:15:"sidebar-primary";s:15:"shop_cat_layout";s:4:"full";s:16:"shop_cat_sidebar";s:15:"sidebar-primary";s:17:"products_per_page";s:2:"12";s:15:"product_fitrows";s:1:"1";s:11:"shop_filter";s:1:"0";s:10:"cat_filter";s:1:"0";s:14:"infinitescroll";s:1:"0";s:11:"shop_toggle";s:1:"0";s:12:"shop_excerpt";s:1:"0";s:11:"shop_rating";s:1:"1";s:13:"outofstocktag";s:1:"0";s:16:"shop_hide_action";s:1:"1";s:16:"product_img_flip";s:1:"0";s:22:"product_quantity_input";s:1:"1";s:18:"product_cat_layout";s:1:"4";s:21:"product_cat_img_ratio";s:13:"widelandscape";s:15:"font_shop_title";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:3:"700";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"16px";s:11:"line-height";s:4:"20px";s:5:"color";s:0:"";}s:20:"shop_title_uppercase";s:1:"0";s:21:"shop_title_min_height";s:2:"40";s:14:"shop_img_ratio";s:6:"square";s:18:"product_img_resize";s:1:"1";s:19:"product_simg_resize";s:1:"1";s:11:"shop_slider";s:1:"0";s:18:"choose_shop_slider";s:4:"none";s:19:"shop_cyclone_slider";s:0:"";s:18:"shop_slider_images";a:2:{i:0;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:1:"0";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}i:1;a:11:{s:3:"url";s:0:"";s:5:"title";s:0:"";s:11:"description";s:0:"";s:4:"link";s:0:"";s:4:"sort";s:0:"";s:13:"attachment_id";s:0:"";s:5:"thumb";s:0:"";s:5:"image";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:6:"target";s:1:"0";}}s:16:"shop_slider_size";s:3:"400";s:22:"shop_slider_size_width";s:4:"1140";s:20:"shop_slider_autoplay";s:1:"1";s:21:"shop_slider_pausetime";s:4:"7000";s:15:"shop_trans_type";s:4:"fade";s:21:"shop_slider_transtime";s:3:"600";s:20:"shop_slider_captions";s:1:"0";s:20:"singleproduct_layout";s:6:"normal";s:23:"product_sidebar_default";s:2:"no";s:31:"product_sidebar_default_sidebar";s:15:"sidebar-primary";s:13:"product_radio";s:1:"0";s:11:"product_nav";s:1:"0";s:12:"product_tabs";s:1:"1";s:19:"product_tabs_scroll";s:1:"0";s:16:"ptab_description";s:2:"10";s:15:"ptab_additional";s:2:"20";s:12:"ptab_reviews";s:2:"30";s:10:"ptab_video";s:2:"40";s:13:"custom_tab_01";s:1:"0";s:13:"custom_tab_02";s:1:"0";s:13:"custom_tab_03";s:1:"0";s:16:"related_products";s:1:"1";s:19:"related_item_column";s:1:"4";s:19:"portfolio_permalink";s:0:"";s:18:"portfolio_comments";s:1:"0";s:14:"portfolio_link";s:0:"";s:19:"portfolio_arrow_nav";s:3:"cat";s:20:"portfolio_tax_column";s:1:"4";s:19:"portfolio_tax_items";s:2:"12";s:27:"portfolio_recent_car_column";s:1:"4";s:31:"portfolio_recent_carousel_speed";s:1:"9";s:26:"portfolio_recent_car_items";s:1:"8";s:32:"portfolio_recent_carousel_scroll";s:7:"oneitem";s:15:"post_word_count";s:2:"40";s:14:"close_comments";s:1:"0";s:11:"hide_author";s:1:"1";s:13:"hide_postedin";s:1:"1";s:16:"hide_commenticon";s:1:"1";s:13:"hide_postdate";s:1:"1";s:14:"show_postlinks";s:1:"0";s:19:"blog_infinitescroll";s:1:"0";s:23:"blog_cat_infinitescroll";s:1:"0";s:24:"blogpost_sidebar_default";s:3:"yes";s:20:"post_summery_default";s:12:"img_portrait";s:26:"post_summery_default_image";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:17:"post_head_default";s:5:"image";s:19:"post_author_default";s:2:"no";s:21:"post_carousel_default";s:2:"no";s:25:"blog_similar_random_order";s:1:"0";s:21:"post_carousel_columns";s:1:"3";s:21:"category_post_summary";s:7:"summary";s:25:"category_post_grid_column";s:1:"3";s:15:"blog_cat_layout";s:7:"sidebar";s:16:"blog_cat_sidebar";s:15:"sidebar-primary";s:15:"skin_stylesheet";s:11:"default.css";s:13:"primary_color";s:0:"";s:15:"primary20_color";s:0:"";s:15:"gray_font_color";s:0:"";s:16:"footerfont_color";s:0:"";s:16:"content_bg_color";s:7:"#f2f2f2";s:17:"bg_content_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:17:"content_bg_repeat";s:0:"";s:21:"content_bg_placementx";s:0:"";s:21:"content_bg_placementy";s:0:"";s:15:"topbar_bg_color";s:0:"";s:16:"bg_topbar_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:16:"topbar_bg_repeat";s:0:"";s:20:"topbar_bg_placementx";s:0:"";s:20:"topbar_bg_placementy";s:0:"";s:15:"header_bg_color";s:7:"#bcd1bc";s:16:"bg_header_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:16:"header_bg_repeat";s:0:"";s:20:"header_bg_placementx";s:0:"";s:20:"header_bg_placementy";s:0:"";s:13:"menu_bg_color";s:0:"";s:14:"bg_menu_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:14:"menu_bg_repeat";s:0:"";s:18:"menu_bg_placementx";s:0:"";s:18:"menu_bg_placementy";s:0:"";s:15:"mobile_bg_color";s:0:"";s:16:"bg_mobile_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:16:"mobile_bg_repeat";s:0:"";s:20:"mobile_bg_placementx";s:0:"";s:20:"mobile_bg_placementy";s:0:"";s:16:"feature_bg_color";s:0:"";s:17:"bg_feature_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:17:"feature_bg_repeat";s:0:"";s:21:"feature_bg_placementx";s:0:"";s:21:"feature_bg_placementy";s:0:"";s:15:"footer_bg_color";s:0:"";s:16:"bg_footer_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:16:"footer_bg_repeat";s:0:"";s:20:"footer_bg_placementx";s:0:"";s:20:"footer_bg_placementy";s:0:"";s:14:"boxed_bg_color";s:0:"";s:15:"bg_boxed_bg_img";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:15:"boxed_bg_repeat";s:0:"";s:19:"boxed_bg_placementx";s:0:"";s:19:"boxed_bg_placementy";s:0:"";s:14:"boxed_bg_fixed";s:0:"";s:13:"boxed_bg_size";s:0:"";s:7:"font_h1";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:3:"400";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"38px";s:11:"line-height";s:4:"40px";s:5:"color";s:0:"";}s:7:"font_h2";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:3:"400";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"32px";s:11:"line-height";s:4:"40px";s:5:"color";s:0:"";}s:7:"font_h3";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:3:"400";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"28px";s:11:"line-height";s:4:"40px";s:5:"color";s:0:"";}s:7:"font_h4";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:3:"400";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"24px";s:11:"line-height";s:4:"40px";s:5:"color";s:0:"";}s:7:"font_h5";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:0:"";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"18px";s:11:"line-height";s:4:"24px";s:5:"color";s:0:"";}s:6:"font_p";a:9:{s:11:"font-family";s:0:"";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:0:"";s:10:"font-style";s:3:"400";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"14px";s:11:"line-height";s:4:"20px";s:5:"color";s:0:"";}s:11:"menu_search";s:1:"0";s:9:"menu_cart";s:1:"0";s:17:"font_primary_menu";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:3:"400";s:10:"font-style";s:0:"";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"16px";s:11:"line-height";s:4:"18px";s:5:"color";s:0:"";}s:23:"primarymenu_hover_color";s:0:"";s:26:"primarymenu_hover_bg_color";s:0:"";s:19:"font_secondary_menu";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:3:"400";s:10:"font-style";s:0:"";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"18px";s:11:"line-height";s:4:"22px";s:5:"color";s:0:"";}s:25:"secondarymenu_hover_color";s:0:"";s:28:"secondarymenu_hover_bg_color";s:0:"";s:19:"secondary_menu_size";s:5:"16.5%";s:19:"dropdown_font_color";s:0:"";s:25:"dropdown_background_color";s:0:"";s:21:"dropdown_border_color";s:0:"";s:15:"show_mobile_btn";s:1:"1";s:23:"mobile_submenu_collapse";s:1:"1";s:16:"font_mobile_menu";a:9:{s:11:"font-family";s:4:"Lato";s:12:"font-options";s:0:"";s:6:"google";s:1:"1";s:11:"font-weight";s:3:"400";s:10:"font-style";s:0:"";s:7:"subsets";s:0:"";s:9:"font-size";s:4:"16px";s:11:"line-height";s:4:"20px";s:5:"color";s:0:"";}s:22:"mobilemenu_hover_color";s:0:"";s:25:"mobilemenu_hover_bg_color";s:0:"";s:16:"mobile_menu_text";s:0:"";s:23:"search_placeholder_text";s:0:"";s:21:"cart_placeholder_text";s:0:"";s:21:"sold_placeholder_text";s:0:"";s:21:"sale_placeholder_text";s:0:"";s:18:"post_readmore_text";s:0:"";s:12:"post_by_text";s:0:"";s:15:"post_incat_text";s:0:"";s:15:"filter_all_text";s:0:"";s:16:"shop_filter_text";s:0:"";s:21:"portfolio_filter_text";s:0:"";s:20:"description_tab_text";s:0:"";s:23:"description_header_text";s:0:"";s:31:"additional_information_tab_text";s:0:"";s:34:"additional_information_header_text";s:0:"";s:14:"video_tab_text";s:0:"";s:16:"video_title_text";s:0:"";s:16:"reviews_tab_text";s:0:"";s:21:"related_products_text";s:0:"";s:21:"lightbox_loading_text";s:0:"";s:16:"lightbox_of_text";s:0:"";s:19:"lightbox_error_text";s:0:"";s:21:"show_breadcrumbs_shop";s:1:"0";s:24:"show_breadcrumbs_product";s:1:"0";s:21:"show_breadcrumbs_post";s:1:"0";s:26:"show_breadcrumbs_portfolio";s:1:"0";s:21:"show_breadcrumbs_page";s:1:"0";s:20:"home_breadcrumb_text";s:0:"";s:9:"blog_link";s:0:"";s:16:"shop_breadcrumbs";s:1:"0";s:13:"page_comments";s:1:"0";s:22:"testimonial_single_nav";s:1:"0";s:16:"testimonial_page";s:0:"";s:17:"hide_image_border";s:1:"1";s:14:"select2_select";s:1:"1";s:21:"virtue_custom_favicon";a:5:{s:3:"url";s:0:"";s:2:"id";s:0:"";s:6:"height";s:0:"";s:5:"width";s:0:"";s:9:"thumbnail";s:0:"";}s:13:"contact_email";s:20:"webmaster@tpginc.net";s:11:"footer_text";s:35:"[copyright] [the-year] [site-name] ";s:14:"search_sidebar";s:15:"sidebar-primary";s:13:"search_layout";s:4:"grid";s:13:"cust_sidebars";a:1:{i:0;s:0:"";}s:14:"page_max_width";s:1:"0";s:16:"smooth_scrolling";s:1:"0";s:21:"smooth_scrolling_hide";s:1:"0";s:27:"smooth_scrolling_background";s:1:"0";s:14:"virtue_gallery";s:1:"1";s:22:"virtue_gallery_masonry";s:1:"1";s:16:"gallery_captions";s:1:"0";s:17:"virtue_animate_in";s:1:"1";s:16:"kadence_lightbox";s:1:"0";s:16:"google_analytics";s:0:"";s:10:"seo_switch";s:1:"0";s:13:"seo_sitetitle";s:0:"";s:19:"seo_sitedescription";s:0:"";s:10:"custom_css";s:0:"";s:10:"rev_slider";s:6:"select";s:9:"kt_slider";s:6:"select";s:17:"mobile_rev_slider";s:6:"select";s:15:"shop_rev_slider";s:6:"select";s:21:"sitewide_calltoaction";i:0;s:21:"sitewide_action_color";s:0:"";s:25:"sitewide_action_btn_color";s:0:"";s:24:"sitewide_action_bg_color";s:0:"";s:31:"sitewide_action_btn_color_hover";s:0:"";s:30:"sitewide_action_bg_color_hover";s:0:"";s:23:"sitewide_action_padding";s:2:"20";s:23:"img_menu_height_setting";s:6:"normal";s:31:"home_custom_carousel_imageratio";i:0;s:21:"kadence_woo_extension";i:1;s:27:"kadence_portfolio_extension";i:1;s:23:"kadence_staff_extension";i:1;s:29:"kadence_testimonial_extension";i:1;s:21:"portfolio_tax_masonry";i:0;s:22:"portfolio_tax_lightbox";i:1;s:26:"portfolio_type_under_title";i:1;s:26:"portfolio_tax_show_excerpt";i:0;s:15:"menu_search_woo";i:0;s:31:"kadence_header_footer_extension";i:0;s:18:"mobile_tablet_show";i:0;s:17:"show_subindicator";i:0;s:16:"postlinks_in_cat";s:3:"all";s:22:"m_center_sticky_header";i:0;s:19:"kt_revslider_notice";i:1;s:26:"hide_rev_activation_notice";i:1;s:23:"kt_cycloneslider_notice";i:1;s:23:"kt_kadenceslider_notice";i:1;s:19:"portfolio_tax_order";s:10:"menu_order";}', 'yes');
"""

    def setup(self,):
        '''(wpm.setup) setup for each test'''

        self.wpm=wp_migrate.WPMigrate()
        #global init
        #self.init = init
 #       init = IniSetup()

        #assert True == False

    @unittest.skip('')
    def test_prompts(self,):
        '''(wpm.test_prompts) verify the prompt routines'''
        print('(test_wpm.prompts)')

        #buffer responses to cmd  prompts
#        ans_pipe = subprocess.Popen('xxx viewproject',shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, universal_newlines=True)
#        _newline = os.linesep
#        _responses = ['data/test/','','www.tpginc.net','www.test.net']
#        ans_pipe.communicate(_newline.join(_responses))

#        wpm.config_parser_values()

#        assert cfg.path,_responses[0])

    def test_pre_pst_proc_rec(self,):
        '''(wpm.test_pre_pst_proc) test the sql processing (syntax errors)'''
        print('(test_wpm.pre_pst_proc)')
        #_r = self.trec1_a.replace("""\', ""","~#~#")
        #_r = _r.replace("~#~#'a","', 'a")
        _q = re.split(r"\\\'\, ",self.trec1_a)
        print('split',_q)

        _x = re.findall(r'\"*(\\\'\, )*"',self.trec1_a)
        print('find',_x)

        _r = re.sub(r"\'\, ",r"~#~#",self.trec1_a)
        #_r = self.wpm.pre_proc_rec(self.trec1_a)
        print('b4:',self.trec1_a)
        print('af:',_r)
        print('sb:',self.trec1_b)
        assert _r == self.trec1_b
        _r = _r.replace("~#~#","""\\', """)
        _r = self.wpm.pst_proc_rec(_r)
        assert _r == self.trec1_a
        assert 0

    @unittest.skip('')
    def test_process_sql(self,):
        '''(wpm.test_process_sql) test the sql processing (syntax errors)'''
        print('(test_wpm.process)')
        self.wpm.process_sql_file()
        assert True == True

    @unittest.skip('')
    def test_edit_rec(self,):
        '''(wpm.test_process_sql) test the sql processing '''
        print('(test_wpm.edit_rec)')
        print('test domain')
        _trec1 = self.wpm.edit_rec(init.test_rec1)
        assert init.test_rec1 == _trec1

        print('test domain without serialization')
        _trec3 = self.wpm.edit_rec(test_rec3)
        assert test_rec3 == _trec3

        print('test prefix')
        _trec2 = self.wpm.edit_rec(test_rec2)
        assert test_rec2 == _trec2

        print('test full path')
        _trec3 = self.wpm.edit_rec(test_rec3)
        assert test_rec3 == _trec3

        assert False == True


    @unittest.skip('')
    def test_sample_skip(self,):
        '''(wpm.sample_skip) test skip a test'''

        print('(test_wpm.sample_skip)')

        assert True == True






