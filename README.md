# Yapay Zeka ile Nükleer Tesislerin Siber Güvenliğinin Sağlanması

**Önemli Not:** Projeye ait detaylı analizler ve demodan görseller için lütfen **ssler** klasörüne bakınız.


**Sistem Analizi ve Tasarımı Dersi Dönem Projesi**

## Proje Ekibi
- Mehmet Hallaç (221120221060)
- Zehra Cıroğlu (221120221010)
- Eren Savaşır (221120221052)
- Abdülsamet Ünverdi (221120221050)
- Tunay Yıldız (221120221031)

## Proje Özeti
Bu projede, nükleer tesislerdeki siber güvenliğin önemi ve zorlukları ele alınmakta ve bu zorlukları yapay zeka kullanarak nasıl aşabileceğimiz araştırılmaktadır. Siber güvenlik ve nükleer tesislerle ilgili temel bilgiler ve makine öğrenmesi algoritmalarını açıklayarak konunun anlaşılmasını sağladıktan sonra, projeyi geliştirme sürecimizi, hangi algoritmayı neden kullandığımızı ve bu algoritmaların başarı oranlarını detaylıca açıklayacağız.

## Motivasyon
Nükleer tesislerin siber güvenliğinin sağlanması, diğer tesislere göre daha zordur. Bunun nedeni, nükleer tesislerde yapılan penetrasyon testlerinin işleyişi bozabileceği ve maddi kayıplara yol açabileceği için yılda 1-2 kez test yapılmasıdır. Bu da tesisin güncel güvenlik açıklarına karşı savunmasız kalmasına yol açmaktadır. Bu projede, nükleer tesislere yapılabilecek üç ana saldırı tipini tespit etmeyi ve bu saldırıları yapay zeka ile önlemeyi amaçladık.

## Saldırı Türleri ve Tespiti
1. **IT Saldırıları**: HMI’dan PLC’ye erişimi engelleyen, ağ içinde sahte paketler ile yoğunluk yaratarak iletişimi yavaşlatan saldırılar. Tespitte, Cycle Time dalgalanmaları incelenir.
2. **ICS Saldırıları**: PLC’leri kapatmak için paket taklidi yaparak komutlar veren saldırılar. PLC’lerin anlık durum verileri ve s7comn veri tipleri üzerinde odaklanılır.
3. **NPP Saldırıları**: En tehlikeli saldırılar olup, örnek olarak Stuxnet saldırısı verilebilir. Tespit için, yapay zekaya normal ve saldırı verilerini verilerek anomali tespit edilmesi sağlanır.

## Metodoloji
Siemens PLCsim, TIA Portal ve MATLAB Simulink kullanarak ağ trafiği, PLC ve proses verilerini topladık. Yapay zekayı, normal ve saldırı verilerini karşılaştırarak anomali tespit etmesi için eğittik. İnternet hızının düşük olmasına rağmen, yapay zeka NPP saldırılarını %70 başarı oranıyla tespit etmeyi başardı.

## Kullanılan Makine Öğrenmesi Modelleri
- **Random Forest**: Karar ağaçlarının topluluğu, aşırı uyumu azaltır.
- **SVM (Support Vector Machine)**: Veriyi sınıflandırmak için en iyi ayrım çizgisini bulur.
- **Gradient Boosting**: Önceki ağaçların hatalarını düzeltmek için ağaçlar sıralı olarak eklenir.
- **Logistic Regression**: İkili sınıflandırma problemleri için kullanılır.
- **XGBoost**: Optimize edilmiş Gradient Boosting versiyonudur.
- **ANNs (Artificial Neural Networks)**: Özellikle karmaşık ve büyük veri setlerinde etkilidir.
- **LSTM (Long Short-Term Memory)**: Zaman serisi verileriyle çalışmak için tasarlanmış bir RNN türüdür.

## Veri Ön İşleme
Veriler, numerik hale getirilip normal ve anormal olarak sınıflandırıldı. Ağ trafiği verileri IP adresine göre, PLC verileri ise çalışma durumuna göre sınıflandırıldı. Proses verileri, normal ve saldırı anındaki verilerle etiketlendi.

## Sonuçlar ve Gelecek Çalışmalar
Yapay zeka, IT ve ICS saldırılarını yüksek doğrulukla tespit ederken, NPP saldırılarında %70 başarı oranı elde etti. Gelecekte, verilerin çeşitliliğini ve hacmini artırarak başarı oranını iyileştirmeyi hedefliyoruz.

## Kullanılan Araçlar ve Yazılımlar
- **Siemens PLCsim ve TIA Portal**
- **MATLAB Simulink**
- **Wireshark** (Ağ izleme)
- **Kaggle** (Model eğitimi)
- **Python** (Simülasyon ve veri çekme)

## Teşekkürler
Bu proje, aşağıdaki kaynaklardan yararlanılarak gerçekleştirilmiştir:
- [Asherah Nükleer Güç Santrali Simülatörü Geliştirme](https://www.semanticscholar.org/paper/DEVELOPMENT-OF-THE-ASHERAH-NUCLEAR-POWER-PLANT-FOR-Silva/215eb3868e595d81fe75496618fae8aebc80674a)
- [IAEA Konferans Makalesi](https://conferences.iaea.org/event/181/contributions/15642/attachments/8548/11374/cn274_Full_Paper_Rodney_Busquim_e_Silva_ANS_Final.pdf)

## Sonuç
Yapay zeka tabanlı sistemimiz, nükleer tesislerin siber güvenliğini artırmak için güçlü bir yaklaşım sunmaktadır. İlk sonuçlarımız, gelecekteki gelişmeler için sağlam bir temel olduğunu göstermektedir.
