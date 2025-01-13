class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Поле lessons только для чтения
    is_subscribed = serializers.SerializerMethodField()  # Добавляем поле для подписки

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons', 'is_subscribed']  # Добавлено поле is_subscribed

    def get_lesson_count(self, obj):
        # Возвращаем количество уроков для курса
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        # Проверяем, подписан ли текущий пользователь на курс
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False  # Если пользователь не аутентифицирован, возвращаем False
