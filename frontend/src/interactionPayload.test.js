import test from 'node:test';
import assert from 'node:assert/strict';
import { buildInteractionPayload } from './interactionPayload.js';
const form = { hcpId: '1', interactionDate: '2026-10-01', summary: '  Demo notes  ', products: ' Example ', followUpDate: '' };
test('structured form produces the API contract without AI interpretation', () => {
  assert.deepEqual(buildInteractionPayload(form), { hcp_id: 1, interaction_date: '2026-10-01', summary: 'Demo notes', products_discussed: 'Example', follow_up_date: null });
});
test('explicit follow-up is retained', () => {
  assert.equal(buildInteractionPayload({ ...form, followUpDate: '2026-10-05' }).follow_up_date, '2026-10-05');
});
for (const hcpId of ['', '0', '-1', '1.5', '1abc', '9007199254740993']) {
  test(`reject invalid ID ${JSON.stringify(hcpId)}`, () => assert.throws(() => buildInteractionPayload({ ...form, hcpId })));
}
test('blank summary is rejected', () => assert.throws(() => buildInteractionPayload({ ...form, summary: '  ' })));
test('oversized summary is rejected', () => assert.throws(() => buildInteractionPayload({ ...form, summary: 'x'.repeat(10001) })));
test('interaction date is required', () => assert.throws(() => buildInteractionPayload({ ...form, interactionDate: '' })));
test('earlier follow-up is rejected', () => assert.throws(() => buildInteractionPayload({ ...form, followUpDate: '2026-09-01' })));
