function onFormSubmit(e) {
  var responses = e.response.getItemResponses();
  var data = {};
  responses.forEach(function(r){ data[r.getItem().getTitle()] = r.getResponse(); });
  var doc = DocumentApp.create("Plan natation - " + (data["Nom"] || "Athlète"));
  doc.getBody().appendParagraph("Programme automatique pour " + data["Nom"]);
  doc.getBody().appendParagraph("Objectif: " + data["Objectif"]);
  var pdf = DriveApp.getFileById(doc.getId()).getAs("application/pdf");
  MailApp.sendEmail({
    to: data["Email"],
    subject: "Ton plan personnalisé",
    htmlBody: "Voici ton plan PDF. Bon entraînement !",
    attachments: [pdf]
  });
}
