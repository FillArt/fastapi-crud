from sqladmin import Admin, ModelView

from app.models import Contact, Author, Category, Post
from app.models.content import PostContent


class ContactAdmin(ModelView, model=Contact):
    column_list = [
        Contact.id,
        Contact.name,
        Contact.email,
        Contact.age,
        Contact.institution,
        Contact.about,
        Contact.file_path
    ]

class AuthorAdmin(ModelView, model=Author):
    column_list = [
        Author.id,
        Author.name,
        Author.last_name,
        Author.middle_name,
        Author.profession,
        Author.avatar_path
    ]

    column_labels = {
        Author.id: "ID",
        Author.name: "Имя",
        Author.last_name: "Фамилия",
        Author.middle_name: "Отчество",
        Author.profession: "Профессия",
        Author.avatar_path: "Аватар (путь)",
    }

    form_columns = [
        Author.name,
        Author.last_name,
        Author.middle_name,
        Author.profession,
        Author.avatar_path
    ]

    column_searchable_list = [Author.name, Author.last_name, Author.profession]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.posts]
    column_labels = {
        Category.id: "ID",
        Category.name: "Название",
        Category.posts: "Посты"
    }

class PostAdmin(ModelView, model=Post):
    column_list = [
        Post.id,
        Post.title,
        Post.author,
        Post.is_published,
        Post.categories,
        Post.created_at
    ]

    column_labels = {
        Post.id: "ID",
        Post.title: "Заголовок",
        Post.description: "Описание",
        Post.author: "Автор",
        Post.is_published: "Опубликовано",
        Post.categories: "Категории",
        Post.image_path: "Изображение",
        Post.created_at: "Создано",
    }

    form_columns = [
        Post.title,
        Post.description,
        Post.author,
        Post.categories,
        Post.is_published,
        Post.image_path
    ]

    column_searchable_list = [Post.title, Post.description]
    column_sortable_list = [Post.created_at, Post.is_published]
    column_default_sort = (Post.created_at, True)

class PostContentAdmin(ModelView, model=PostContent):
    column_list = [
        PostContent.id,
        PostContent.post_id,
        PostContent.type,
        PostContent.value,
        PostContent.order
    ]

    column_labels = {
        PostContent.id: "ID",
        PostContent.post_id: "Пост",
        PostContent.type: "Тип",
        PostContent.value: "Значение (JSON)",
        PostContent.order: "Порядок"
    }

    form_columns = [
        PostContent.post_id,
        PostContent.type,
        PostContent.value,
        PostContent.order
    ]

    column_sortable_list = [PostContent.order]

def setup_admin(app, engine):
    admin = Admin(app, engine)

    admin.add_view(ContactAdmin)
    admin.add_view(AuthorAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(PostContentAdmin)

    return admin
