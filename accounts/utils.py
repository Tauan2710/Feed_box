def usuario_tem_acesso(feedback, user):
    if user.perfil.is_master:
        return True
    return feedback.setor == user.perfil.setor
