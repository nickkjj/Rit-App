from rest_framework import serializers
from table_administration_service.models.question_models import Question, QuestionVersion
from table_administration_service.serializers.employee_serializers import EmployeeReadSerializer


class QuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'weight']

class QuestionVersionReadSerializer(serializers.ModelSerializer):

    questions = QuestionReadSerializer(many=True, read_only=True)
    created_by = EmployeeReadSerializer(read_only=True)

    class Meta:
        model = QuestionVersion
        fields = ['id', 'created_at', 'created_by', 'status', 'questions']

class QuestionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['title', 'weight']

class QuestionVersionCreateSerializer(serializers.ModelSerializer):

    questions = QuestionCreateSerializer(many=True)
    created_by = EmployeeReadSerializer(read_only=True)

    class Meta:
        model = QuestionVersion
        fields = ['questions', 'created_by']

    def validate(self, data):
        #separando as questões do json
        questions_data = data.get('questions', [])

        #somando total dos pesos das questões
        total_weight = sum([q['weight'] for q in questions_data])

        #verificando se a soma é 100
        if total_weight != 100:
            raise serializers.ValidationError("A soma dos pesos das questões tem que resultar em 100.")

        return data


    def create(self, validated_data):
        
        #encontrando usuario que está logado
        user = self.context['request'].user

        #adicionando usuario ao validated_data
        validated_data['created_by'] = user
        
        #separando os dados das questões e versão
        questions_data = validated_data.pop('questions') 

        #desativando a versão antiga
        QuestionVersion.objects.filter(status=True).update(status=False)

        #criando a versão
        version = QuestionVersion.objects.create(**validated_data)

        #instanciando as questões em uma lista e vinculando elas à versão nova
        questions_to_create = [Question(questions_version=version, **q_data) for q_data in questions_data] 

        #criando todas questões simultaneamente com bulk
        Question.objects.bulk_create(questions_to_create)

        return version