# App de Autenticação Customizada (custom_auth)

O app **`custom_auth`** é responsável por gerenciar a autenticação personalizada dos usuários, substituindo o modelo padrão de autenticação do Django por um modelo mais flexível. O app permite que os usuários criem contas, façam login, editem seus perfis, e gerenciem suas redes sociais.

## Funcionalidades

- **Modelos Customizados**: Modelo de usuário extendido (`User`) e perfil de usuário (`UserProfile`).
- **Autenticação Customizada**: Formulários para login e criação de usuários, com validação personalizada.
- **Perfis de Usuário**: Os usuários podem gerenciar dados pessoais e redes sociais em suas configurações.
- **Diferentes Níveis de Usuários**: Free, Pro e Ultra, com propriedades específicas em cada nível.

## Modelos

### `User`

O modelo de usuário customizado herda de `AbstractUser` e adiciona campos personalizados, como biografia e links de redes sociais:

```python
class User(AbstractUser):
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    @property
    def is_pro(self):
        return self.profile.is_pro

    @property
    def is_ultra(self):
        return self.profile.is_ultra

    def __str__(self):
        return self.username
```

* **Campos Customizados** : `bio`, `website`, `github`, `twitter`, `linkedin`, e `profile_picture` permitem uma personalização adicional para cada usuário.
* **Permissões e Grupos** : Os campos `groups` e `user_permissions` foram redefinidos para evitar conflitos com o modelo padrão.

### `UserProfile`

O `UserProfile` define diferentes tipos de usuários, como Free, Pro e Ultra, oferecendo funcionalidades adicionais para usuários avançados.

```python
class UserProfile(models.Model):
    FREE = 'free'
    PRO = 'pro'
    ULTRA = 'ultra'
  
    USER_TYPES = [
        (FREE, 'Free User'),
        (PRO, 'Pro User'),
        (ULTRA, 'Ultra User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default=FREE)

    @property
    def is_free(self):
        return self.user_type == self.FREE

    @property
    def is_pro(self):
        return self.user_type == self.PRO

    @property
    def is_ultra(self):
        return self.user_type == self.ULTRA
```

* **`user_type`** : Define o tipo de conta do usuário. Isso é importante para determinar os recursos disponíveis para cada tipo de usuário.

## Formulários

Os formulários são utilizados para gerenciar a autenticação e edição de perfis de usuários.

### `CustomLoginForm`

Formulário de login com validação personalizada:

```python
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nome de Usuário', ...)
    password = forms.CharField(label='Senha', ...)
  
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
  
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Nome de usuário ou senha incorretos.")
        return cleaned_data
```

### `CustomUserCreationForm`

Formulário de criação de novos usuários:

```python
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
```

### `PersonalDataForm`

Formulário para atualizar dados pessoais do usuário:

```python
class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']
```

### `SocialMediaForm`

Formulário para atualizar as redes sociais do usuário:

```python
class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['website', 'github', 'twitter', 'linkedin']
```

## Views

As views principais controlam o fluxo de autenticação, registro e configuração de perfis.

### `login_view`

A view de login processa o formulário e autentica o usuário:

```python
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('pages:home')
        else:
            messages.error(request, 'Erro ao fazer login.')
    else:
        form = CustomLoginForm()
  
    return render(request, 'custom_auth/login.html', {'form': form})
```

### `register`

A view de registro cria um novo usuário:

```python
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('pages:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'custom_auth/register.html', {'form': form})
```

### `settings`

A view de configurações permite que os usuários atualizem seus dados pessoais e redes sociais:

```python
@login_required
def settings(request):
    if request.method == 'POST':
        personal_form = PersonalDataForm(request.POST, request.FILES, instance=request.user)
        social_form = SocialMediaForm(request.POST, instance=request.user)
      
        if personal_form.is_valid() and social_form.is_valid():
            personal_form.save()
            social_form.save()
            messages.success(request, 'Configurações atualizadas.')
            return redirect('users:settings')
        else:
            messages.error(request, 'Erro ao salvar as configurações.')
    else:
        personal_form = PersonalDataForm(instance=request.user)
        social_form = SocialMediaForm(instance=request.user)
  
    return render(request, 'custom_auth/settings.html', {
        'personal_form': personal_form,
        'social_form': social_form,
    })

```


## URLs

As rotas principais para autenticação estão definidas no arquivo `custom_auth/urls.py`:

```python
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('pages:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'custom_auth/register.html', {'form': form})

```

## Templates

Os templates estão organizados na pasta `custom_auth/templates/custom_auth/` e incluem:

* **login.html** : Formulário de login.
* **register.html** : Formulário de registro.
* **settings.html** : Formulário de configurações.

## Conclusão

O app **custom_auth** fornece uma solução flexível para gerenciar autenticação e perfis de usuários em um sistema de SaaS. Ele permite a criação de perfis detalhados, a gestão de redes sociais, e a autenticação customizada com diferentes níveis de usuários.
