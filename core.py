import filtres
import player

filtres = filtres.Filtres()

p = player.Player("sounds/a_million_dreams.wav")
stream = p.open_stream()
data = p.get_data()

# Paramètres du filtre (A LIER A L'IHM)
f_c = 2000 # Fréquence de coupure avec omega_c = 2*pi*f_c
ksi = 1.5 # plus il est élevé, plus le filtre de second ordre est large mais attention quand même hein

# Discrétisation par Euler du filtre choisi
filtre_choisi = "R" # R = Rejecteur, P1 = Passe bas ordre 1, H1 = Passe haut ordre 1, P2 = Passe bas ordre 2, H2 = Passe haut ordre 2
B_z, A_z = filtres.go_filtre(filtre_choisi, f_c, Fs=p.Fs, ksi=ksi)

# Filtrage du premier chunk
data_bytes_filt, s_e, s_s = filtres.traitement_chunk(data, A_z=A_z, B_z=B_z)

print("Lecture de l'audio...")

# Lecture et filtrage des chunks suivants
while len(data) != 0:
    stream.write(data_bytes_filt) # écriture des 1024 bits filtrés
    data = p.get_data()
    # Filtrage du nouveau chunk
    data_bytes_filt = filtres.traitement_chunk(data, A_z=A_z, B_z=B_z, s_e=s_e, s_s=s_s)
    # TODO ajout de la variation de la fréquence de coupure
    # Note à moi-même : Genre il faudrait qu'à chaque tour de boucle, on vérifie si la fréquence ou ksi a changé
    # Et si oui, on recalcule le filtre (filtres.go_filtre(filtre_choisi, f_c etc...)) pour le réappliquer
    # Juste pas le temps de le faire maintenant j'ai une vie

print("Fin de lecture.")
stream.stop_stream()
stream.close()

p.terminate()