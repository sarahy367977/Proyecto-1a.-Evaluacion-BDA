DROP TABLE users CASCADE CONSTRAINTS;
DROP TABLE articles CASCADE CONSTRAINTS;
DROP TABLE comments CASCADE CONSTRAINTS;
DROP TABLE tags CASCADE CONSTRAINTS;
DROP TABLE categories CASCADE CONSTRAINTS;
DROP TABLE article_tags CASCADE CONSTRAINTS;
DROP TABLE article_categories CASCADE CONSTRAINTS;

-- TABLAS
create table users (
    id number primary key,
    name varchar2(100) not null,
    email varchar2(150)
);

create table articles (
    id number primary key,
    title varchar2(200) not null,
    article_date date default sysdate,
    text clob,
    user_id number references users(id)
);

create table comments (
    id number primary key,
    article_id number references articles(id),
    name varchar2(100) not null,
    text clob,
    comment_date date default sysdate
);

create table tags (
    id number primary key,
    name varchar2(100) not null,
    url varchar2(200)
);

create table categories (
    id number primary key,
    name varchar2(100) not null,
    url varchar2(200)
);

create table article_tags (
    article_id number references articles(id),
    tag_id number references tags(id),
    primary key(article_id, tag_id)
);

create table article_categories (
    article_id number references articles(id),
    category_id number references categories(id),
    primary key(article_id, category_id)
);

-- FUNCIONES Y PROCEDIMIENTOS PL/SQL
create or replace function register_user(
    p_name in varchar2,
    p_email in varchar2
) return number is
    v_id number;
begin
    select nvl(max(id),0)+1 into v_id from users;
    insert into users (id, name, email) values (v_id, p_name, p_email);
    return v_id;
end register_user;
/

create or replace function create_tag(
    p_name in varchar2,
    p_url in varchar2 default null
) return number is
    v_id number;
begin
    select nvl(max(id),0)+1 into v_id from tags;
    insert into tags (id, name, url) values (v_id, p_name, p_url);
    return v_id;
end create_tag;
/

create or replace function create_category(
    p_name in varchar2,
    p_url in varchar2 default null
) return number is
    v_id number;
begin
    select nvl(max(id),0)+1 into v_id from categories;
    insert into categories (id, name, url) values (v_id, p_name, p_url);
    return v_id;
end create_category;
/

create or replace function add_article(
    p_title in varchar2,
    p_text in clob,
    p_user_id in number
) return number is
    v_id number;
begin
    select nvl(max(id),0)+1 into v_id from articles;
    insert into articles (id, title, text, article_date, user_id)
    values (v_id, p_title, p_text, sysdate, p_user_id);
    return v_id;
end add_article;
/

create or replace procedure add_comment(
    p_article_id in number,
    p_user_id in number,
    p_text in clob
) is
    v_user_name varchar2(100);
    v_comment_id number;
begin
    select name into v_user_name from users where id = p_user_id;
    select nvl(max(id),0)+1 into v_comment_id from comments;
    insert into comments (id, article_id, name, text, comment_date)
    values (v_comment_id, p_article_id, v_user_name, p_text, sysdate);
end add_comment;
/

create or replace procedure add_tag_to_article(
    p_article_id in number,
    p_tag_id in number
) is
begin
    insert into article_tags (article_id, tag_id) values (p_article_id, p_tag_id);
exception
    when dup_val_on_index then null;
end add_tag_to_article;
/

create or replace procedure add_category_to_article(
    p_article_id in number,
    p_category_id in number
) is
begin
    insert into article_categories (article_id, category_id) values (p_article_id, p_category_id);
exception
    when dup_val_on_index then null;
end add_category_to_article;
/

create or replace procedure delete_article_complete(
    p_article_id in number
) is
begin
    delete from article_tags where article_id = p_article_id;
    delete from article_categories where article_id = p_article_id;
    delete from comments where article_id = p_article_id;
    delete from articles where id = p_article_id;
    commit;
end delete_article_complete;
/

create or replace function count_comments(p_article_id in number) 
return number is
    v_count number;
begin
    select count(*) into v_count from comments where article_id = p_article_id;
    return v_count;
end count_comments;
/

create or replace function get_articles return sys_refcursor is
    v_cursor sys_refcursor;
begin
    open v_cursor for 
    select a.id, a.title, a.article_date, u.name as author 
    from articles a, users u 
    where a.user_id = u.id 
    order by a.article_date desc;
    return v_cursor;
end get_articles;
/
