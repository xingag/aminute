/**
 * Created by Administrator on 2016/12/17.
 */

$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if (that.children('a').attr('href') == '#') {
            event.preventDefault();
        }
        if (that.parent().hasClass('unfold')) {
            that.parent().removeClass('unfold');
        } else {
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration', 'none');
    });
});


// 前端和后台的配合
// 前端通过后台定义的url来改变cms后台页面的选中展开样式
$(function () {
    var url = window.location.href;
    if (url.indexOf('profile') >= 0) {
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('reset_pwd') >= 0) {
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('reset_email') >= 0) {
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('posts') >= 0) {
        var postManageLi = $('.post-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('boards') >= 0) {
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('permissions') >= 0) {
        var permissionManageLi = $('.permission-manage');
        permissionManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('roles') >= 0) {
        var roleManageLi = $('.role-manage');
        roleManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('front_users') >= 0) {
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('cms_users') >= 0) {
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('cms_group') >= 0) {   //开发者 - CMS组管理【最高权限】
        var cmsroleManageLi = $('.cmsrole-manage');
        cmsroleManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('banners') >= 0) {
        var bannerManageLi = $('.banner-manage');
        bannerManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('news')>=0){
        var newsManageLi = $('.news-manage');
        newsManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});