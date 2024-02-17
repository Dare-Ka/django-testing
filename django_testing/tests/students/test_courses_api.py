import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    courses = course_factory(_quantity=10)

    for i in range(10):
        response = client.get(f'/api/v1/courses/{i + 1}/')
        data = response.json()
        assert response.status_code == 200
        assert data['name'] == courses[i].name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


@pytest.mark.django_db
def test_filters_id_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    for i in range(10):
        response = client.get(f'/api/v1/courses/?id={courses[i].id}')
        data = response.json()
        print(data)
        assert data[0]['id'] == courses[i].id


@pytest.mark.django_db
def test_filters_name_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    for i in range(10):
        response = client.get(f'/api/v1/courses/?name={courses[i].name}')
        data = response.json()
        print(data)
        assert data[0]['name'] == courses[i].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name': 'Python'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()

    response = client.patch(f'/api/v1/courses/{course.id}/', data={'name': 'Python'})
    assert response.status_code == 200
    assert course.name == 'Python'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()
    count = Course.objects.count()

    response = client.delete(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1







