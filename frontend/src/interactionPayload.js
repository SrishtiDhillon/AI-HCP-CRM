export function buildInteractionPayload(form) {
  const rawId = String(form.hcpId).trim();
  if (!/^[1-9]\d*$/.test(rawId) || !Number.isSafeInteger(Number(rawId))) {
    throw new Error('Enter a positive whole-number HCP ID.');
  }
  const summary = form.summary.trim();
  if (!summary) throw new Error('Enter an interaction summary.');
  if (summary.length > 10000) throw new Error('Summary must be 10,000 characters or fewer.');
  if (!form.interactionDate) throw new Error('Choose an interaction date.');
  if (form.followUpDate && form.followUpDate < form.interactionDate) {
    throw new Error('Follow-up date cannot precede interaction date.');
  }
  return {
    hcp_id: Number(rawId),
    interaction_date: form.interactionDate,
    summary,
    products_discussed: form.products.trim(),
    follow_up_date: form.followUpDate || null,
  };
}
