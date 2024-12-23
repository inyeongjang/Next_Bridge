from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from home.models import Question, Answer, Comment
from common.forms import UserForm, UserProfileForm
from common.models import UserProfile

# 프로필 기본정보
def profile_base(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    user_profile = profile_user.profile  # UserProfile 객체

    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'profile_type': 'base'
    }
    return render(request, 'common/profile/profile_base.html', context)


# 프로필 목록 추상 클래스 뷰
class ProfileObjectListView(ListView):
    paginate_by = 10

    class Meta:
        abstract = True

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        self.so = self.request.GET.get('so', 'recent')  # 정렬기준
        object_list = self.model.objects.filter(author=self.profile_user)
        # 정렬
        object_list = Answer.order_by_so(object_list, self.so)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_user': self.profile_user,
            'profile_type': self.profile_type,
            'so': self.so
        })
        return context


# 작성한 질문 목록
class ProfileQuestionListView(ProfileObjectListView):
    model = Question
    template_name = 'common/profile/profile_question.html'
    profile_type = 'question'


# 작성한 답변 목록
class ProfileAnswerListView(ProfileObjectListView):
    model = Answer
    template_name = 'common/profile/profile_answer.html'
    profile_type = 'answer'


# 작성한 댓글 목록
class ProfileCommentListView(ProfileObjectListView):
    model = Comment
    template_name = 'common/profile/profile_comment.html'
    profile_type = 'comment'


# 추천 목록
class ProfileVoteListView(ProfileObjectListView):
    template_name = 'common/profile/profile_vote.html'
    profile_type = 'vote'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])

        # 질문과 답변을 결합한 쿼리셋
        question_list = self.profile_user.voter_question.all()
        answer_list = self.profile_user.voter_answer.annotate(category=F('question__category__description'))
        combined_list = chain(question_list, answer_list)

        # 정렬 기준 적용
        so = self.request.GET.get('so', 'recent')
        if so == 'recommend':
            sorted_list = sorted(
                combined_list,
                key=lambda obj: getattr(obj, 'voter_count', 0),
                reverse=True,
            )
        else:
            sorted_list = sorted(
                combined_list,
                key=lambda obj: obj.create_date,
                reverse=True,
            )
        return sorted_list


    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context.update({
            'profile_user': self.profile_user,
            'profile_type': self.profile_type,
            'so': self.request.GET.get('so', 'recent')
        })
        return context


@login_required
def profile_edit(request, user_id):
    # 프로필 정보를 가져오는 코드
    profile_user = get_object_or_404(UserProfile, user__id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            # 수정 후 profile_base로 리디렉션할 때 user_id 전달
            return redirect('common:profile_base', user_id=user_id)
    else:
        form = UserProfileForm(instance=profile_user)

    return render(request, 'common/profile/profile_edit.html', {'form': form})