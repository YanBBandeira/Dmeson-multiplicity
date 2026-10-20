#include <iostream>
#include "Pythia8/Pythia.h"
#include <string>
#include <filesystem>

using namespace Pythia8;
namespace fs = std::filesystem;

// Boolean function to identify charm hadrons:
bool isCharmHadron(int id)
{
  int idAbs = abs(id);
  if (idAbs >= 411 && idAbs <= 435)
    return true;
  return false;
}

// Função principal
int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    std::cerr << "Uso: " << argv[0] << "<ecm_em_GeV>" << std::endl;
  }

  std::string eCM_str = argv[1];
  Pythia pythia;

  pythia.readString("Beams:idA = 2212");       // proton
  pythia.readString("Beams:idB = 1000822080"); // lead
  pythia.readString("Beams:eCM = " + eCM_str);

  pythia.readString("HeavyIon:mode = 1");
  // pythia.readString("HeavyIon:AlphaCluster = on");

  pythia.readString("Angantyr:NucleusModelB = 2"); // 2 = Wood-Saxon distribution
  pythia.readString("HeavyIonB:WSR = 6.62");       // Value of the radius parameter R for the Wood-Saxon distribution
  pythia.readString("HeavyIonB:WSa = 0.546");      // Value of the skin depth parameter a for the Wood-Saxon distribution

  pythia.readString("SoftQCD:all = on");
  // pythia.readString("HardQCD:all = on");

  pythia.readString("HadronLevel:all = on");

  // pythia.readString("HardQCD:hardccbar = on");
  // pythia.readString("HardQCD:gg2ccbar = on");
  // pythia.readString("HardQCD:qqbar2ccbar = on");

  pythia.readString("411:mayDecay = off");  // D+
  pythia.readString("-411:mayDecay = off"); // D-
  pythia.readString("421:mayDecay = off");  // D0
  pythia.readString("-421:mayDecay = off"); // D0bar
  pythia.readString("413:mayDecay = off");  // D*+
  pythia.readString("-413:mayDecay = off"); // D*-
  pythia.readString("423:mayDecay = off");  // D*0
  pythia.readString("-423:mayDecay = off"); // D*0bar
  pythia.readString("415:mayDecay = off");  // D2*+
  pythia.readString("-415:mayDecay = off"); // D2*-
  pythia.readString("425:mayDecay = off");  // D2*0
  pythia.readString("-425:mayDecay = off"); // D2*0bar
  pythia.readString("431:mayDecay = off");  // Ds+
  pythia.readString("-431:mayDecay = off"); // Ds-
  pythia.readString("433:mayDecay = off");  // Ds*+
  pythia.readString("-433:mayDecay = off"); // Ds*-
  pythia.readString("435:mayDecay = off");  // Ds2*
  pythia.readString("-435:mayDecay = off"); // Ds2*bar

  if (!pythia.init())
  {
    cout << "Erro: falha na inicialização do Pythia." << endl;
    return 1;
  }
  cout << "Pythia inicializado com sucesso." << endl;

  Hist histcharmTotal0(" ", 100, -0.5, 99.5);
  Hist histcharmTotal1(" ", 100, -0.5, 99.5);
  Hist histcharmTotal2(" ", 100, -0.5, 99.5);
  Hist histcharmTotal3(" ", 100, -0.5, 99.5);
  Hist histcharmTotal4(" ", 100, -0.5, 99.5);
  Hist histcharmTotal5(" ", 100, -0.5, 99.5);
  Hist histcharmTotal6(" ", 100, -0.5, 99.5);
  Hist histcharmTotal7(" ", 100, -0.5, 99.5);
  Hist histcharmTotalAsym(" ", 100, -0.5, 99.5);

  Hist histcFinalPartonLevel0(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel1(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel2(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel3(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel4(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel5(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel6(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevel7(" ", 100, -0.5, 99.5);
  Hist histcFinalPartonLevelAsym(" ", 100, -0.5, 99.5);

  Hist histDmeson0(" ", 100, -0.5, 99.5);
  Hist histDmeson1(" ", 100, -0.5, 99.5);
  Hist histDmeson2(" ", 100, -0.5, 99.5);
  Hist histDmeson3(" ", 100, -0.5, 99.5);
  Hist histDmeson4(" ", 100, -0.5, 99.5);
  Hist histDmeson5(" ", 100, -0.5, 99.5);
  Hist histDmeson6(" ", 100, -0.5, 99.5);
  Hist histDmeson7(" ", 100, -0.5, 99.5);
  Hist histDmesonAsym(" ", 100, -0.5, 99.5);

  int nEvent = 10000; // 1000000;

  for (int iEvent = 0; iEvent < nEvent; ++iEvent)
  {
    if (!pythia.next())
      continue;

    int ncharmTotal0 = 0;
    int ncharmTotal1 = 0;
    int ncharmTotal2 = 0;
    int ncharmTotal3 = 0;
    int ncharmTotal4 = 0;
    int ncharmTotal5 = 0;
    int ncharmTotal6 = 0;
    int ncharmTotal7 = 0;
    int ncharmTotalAsym = 0;

    int ncFinalPartonLevel0 = 0;
    int ncFinalPartonLevel1 = 0;
    int ncFinalPartonLevel2 = 0;
    int ncFinalPartonLevel3 = 0;
    int ncFinalPartonLevel4 = 0;
    int ncFinalPartonLevel5 = 0;
    int ncFinalPartonLevel6 = 0;
    int ncFinalPartonLevel7 = 0;
    int ncFinalPartonLevelAsym = 0;

    int nDmeson0 = 0;
    int nDmeson1 = 0;
    int nDmeson2 = 0;
    int nDmeson3 = 0;
    int nDmeson4 = 0;
    int nDmeson5 = 0;
    int nDmeson6 = 0;
    int nDmeson7 = 0;
    int nDmesonAsym = 0;

    for (int i = 0; i < pythia.event.size(); ++i)
    {

      if (abs(pythia.event[i].id()) == 4)
      {
        double eta = pythia.event[i].eta();
        if (fabs(eta) < 0.5)
          ++ncharmTotal0;
        if (fabs(eta) < 1.0)
          ++ncharmTotal1;
        if (fabs(eta) < 2.0)
          ++ncharmTotal2;
        if (fabs(eta) < 3.0)
          ++ncharmTotal3;
        if (fabs(eta) < 4.0)
          ++ncharmTotal4;
        if (fabs(eta) < 5.0)
          ++ncharmTotal5;
        if (fabs(eta) < 6.0)
          ++ncharmTotal6;
        if (fabs(eta) < 7.0)
          ++ncharmTotal7;
        if (eta > 3.1 && eta < 5.0)
          ++ncharmTotalAsym;
      }

      if (pythia.event[i].isFinalPartonLevel() &&
          abs(pythia.event[i].id()) == 4)
      {
        double eta = pythia.event[i].eta();
        if (fabs(eta) < 0.5)
          ++ncFinalPartonLevel0;
        if (fabs(eta) < 1.0)
          ++ncFinalPartonLevel1;
        if (fabs(eta) < 2.0)
          ++ncFinalPartonLevel2;
        if (fabs(eta) < 3.0)
          ++ncFinalPartonLevel3;
        if (fabs(eta) < 4.0)
          ++ncFinalPartonLevel4;
        if (fabs(eta) < 5.0)
          ++ncFinalPartonLevel5;
        if (fabs(eta) < 6.0)
          ++ncFinalPartonLevel6;
        if (fabs(eta) < 7.0)
          ++ncFinalPartonLevel7;
        if (eta > -3.1 && eta < 5.0)
          ++ncFinalPartonLevelAsym;
      }

      if (pythia.event[i].isFinal() &&
          isCharmHadron(pythia.event[i].id()))
      {
        double eta = pythia.event[i].eta();
        if (fabs(eta) < 0.5)
          ++nDmeson0;
        if (fabs(eta) < 1.0)
          ++nDmeson1;
        if (fabs(eta) < 2.0)
          ++nDmeson2;
        if (fabs(eta) < 3.0)
          ++nDmeson3;
        if (fabs(eta) < 4.0)
          ++nDmeson4;
        if (fabs(eta) < 5.0)
          ++nDmeson5;
        if (fabs(eta) < 6.0)
          ++nDmeson6;
        if (fabs(eta) < 7.0)
          ++nDmeson7;
        if (eta > -3.1 && eta < 5.0)
          ++nDmesonAsym;

        // int id = pythia.event[i].id();
        // cout << "Hádron com charm encontrado: " << id << " - " << pythia.event[i].name() << endl;
      }
    }

    histcharmTotal0.fill(ncharmTotal0);
    histcharmTotal1.fill(ncharmTotal1);
    histcharmTotal2.fill(ncharmTotal2);
    histcharmTotal3.fill(ncharmTotal3);
    histcharmTotal4.fill(ncharmTotal4);
    histcharmTotal5.fill(ncharmTotal5);
    histcharmTotal6.fill(ncharmTotal6);
    histcharmTotal7.fill(ncharmTotal7);
    histcharmTotalAsym.fill(ncharmTotalAsym);

    histcFinalPartonLevel0.fill(ncFinalPartonLevel0);
    histcFinalPartonLevel1.fill(ncFinalPartonLevel1);
    histcFinalPartonLevel2.fill(ncFinalPartonLevel2);
    histcFinalPartonLevel3.fill(ncFinalPartonLevel3);
    histcFinalPartonLevel4.fill(ncFinalPartonLevel4);
    histcFinalPartonLevel5.fill(ncFinalPartonLevel5);
    histcFinalPartonLevel6.fill(ncFinalPartonLevel6);
    histcFinalPartonLevel7.fill(ncFinalPartonLevel7);
    histcFinalPartonLevelAsym.fill(ncFinalPartonLevelAsym);

    histDmeson0.fill(nDmeson0);
    histDmeson1.fill(nDmeson1);
    histDmeson2.fill(nDmeson2);
    histDmeson3.fill(nDmeson3);
    histDmeson4.fill(nDmeson4);
    histDmeson5.fill(nDmeson5);
    histDmeson6.fill(nDmeson6);
    histDmeson7.fill(nDmeson7);
    histDmesonAsym.fill(nDmesonAsym);
  }
  std::string dirOutput = "../../Output/pPb/Soft_pPb/eCM_" + eCM_str + "GeV/";
  fs::create_directories(dirOutput);

  // Salvando os histogramas corretamente com o método .table()
  histcharmTotal0.table(dirOutput + "histcharmTotal0.dat");
  histcharmTotal1.table(dirOutput + "histcharmTotal1.dat");
  histcharmTotal2.table(dirOutput + "histcharmTotal2.dat");
  histcharmTotal3.table(dirOutput + "histcharmTotal3.dat");
  histcharmTotal4.table(dirOutput + "histcharmTotal4.dat");
  histcharmTotal5.table(dirOutput + "histcharmTotal5.dat");
  histcharmTotal6.table(dirOutput + "histcharmTotal6.dat");
  histcharmTotal7.table(dirOutput + "histcharmTotal7.dat");
  histcharmTotalAsym.table(dirOutput + "histcharmTotalAsym.dat");

  histcFinalPartonLevel0.table(dirOutput + "histcFinalPartonLevel0.dat");
  histcFinalPartonLevel1.table(dirOutput + "histcFinalPartonLevel1.dat");
  histcFinalPartonLevel2.table(dirOutput + "histcFinalPartonLevel2.dat");
  histcFinalPartonLevel3.table(dirOutput + "histcFinalPartonLevel3.dat");
  histcFinalPartonLevel4.table(dirOutput + "histcFinalPartonLevel4.dat");
  histcFinalPartonLevel5.table(dirOutput + "histcFinalPartonLevel5.dat");
  histcFinalPartonLevel6.table(dirOutput + "histcFinalPartonLevel6.dat");
  histcFinalPartonLevel7.table(dirOutput + "histcFinalPartonLevel7.dat");
  histcFinalPartonLevelAsym.table(dirOutput + "histcFinalPartonLevelAsym.dat");

  histDmeson0.table(dirOutput + "histDmeson0.dat");
  histDmeson1.table(dirOutput + "histDmeson1.dat");
  histDmeson2.table(dirOutput + "histDmeson2.dat");
  histDmeson3.table(dirOutput + "histDmeson3.dat");
  histDmeson4.table(dirOutput + "histDmeson4.dat");
  histDmeson5.table(dirOutput + "histDmeson5.dat");
  histDmeson6.table(dirOutput + "histDmeson6.dat");
  histDmeson7.table(dirOutput + "histDmeson7.dat");
  histDmesonAsym.table(dirOutput + "histDmesonAsym.dat");

  cout << "Simulação finalizada e arquivos salvos com sucesso e salvos em" + dirOutput + "!" << endl;

  return 0;
}